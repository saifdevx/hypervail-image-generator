"""Reference-image validation and provider-safe normalization.

Hyperex decodes the user's upload once, applies EXIF orientation, and stores a
provider-safe RGB/RGBA JPEG or PNG while preserving the original filename as
metadata.  This prevents provider-specific failures caused by CMYK JPEGs,
palette PNGs, 16-bit images, unusual metadata/encoders, or formats such as
HEIC/TIFF/BMP/GIF that providers do not accept directly.  Older jobs are
normalized lazily when they are retried.
"""

from __future__ import annotations

from io import BytesIO
import mimetypes
from pathlib import Path
import warnings

from PIL import Image, ImageOps, UnidentifiedImageError


# HEIC / HEIF are not decoded by Pillow on every platform.  The project ships
# pillow-heif in requirements.txt; registration is intentionally optional here
# so Hyperex can still start if an older local environment has not installed the
# new dependency yet.  Uploading HEIC/HEIF then produces a clear validation
# message instead of breaking application startup.
_HEIF_ENABLED = False
try:
    import pillow_heif

    pillow_heif.register_heif_opener()

    register_avif = getattr(
        pillow_heif,
        "register_avif_opener",
        None,
    )
    if callable(register_avif):
        register_avif()

    _HEIF_ENABLED = True
except Exception:
    _HEIF_ENABLED = False


MAX_AI_REFERENCE_BYTES = 20 * 1024 * 1024


class ReferenceImageError(ValueError):
    """Raised when a reference cannot be safely decoded/normalized."""


_FORMAT_DETAILS = {
    "JPEG": (".jpg", "image/jpeg"),
    "JPG": (".jpg", "image/jpeg"),
    "PNG": (".png", "image/png"),
    "WEBP": (".webp", "image/webp"),
    "GIF": (".gif", "image/gif"),
    "BMP": (".bmp", "image/bmp"),
    "DIB": (".bmp", "image/bmp"),
    "TIFF": (".tif", "image/tiff"),
    "TIF": (".tif", "image/tiff"),
    "ICO": (".ico", "image/x-icon"),
    "AVIF": (".avif", "image/avif"),
    "HEIF": (".heif", "image/heif"),
    "HEIC": (".heic", "image/heic"),
    "JPEG2000": (".jp2", "image/jp2"),
    "JP2": (".jp2", "image/jp2"),
    "PSD": (".psd", "image/vnd.adobe.photoshop"),
    "TGA": (".tga", "image/x-tga"),
    "DDS": (".dds", "image/vnd-ms.dds"),
    "QOI": (".qoi", "image/qoi"),
    "PCX": (".pcx", "image/x-pcx"),
    "PPM": (".ppm", "image/x-portable-pixmap"),
    "PGM": (".pgm", "image/x-portable-graymap"),
    "PBM": (".pbm", "image/x-portable-bitmap"),
}


def _safe_original_suffix(original_filename: str | None) -> str:
    suffix = Path(original_filename or "").suffix.lower()
    if (
        suffix
        and len(suffix) <= 10
        and suffix[1:].replace("-", "").replace("_", "").isalnum()
    ):
        return suffix
    return ".img"


def _format_details(
    format_name: str | None,
    original_filename: str | None,
) -> tuple[str, str]:
    normalized = (format_name or "").upper()
    mapped = _FORMAT_DETAILS.get(normalized)
    if mapped:
        return mapped

    # Pillow knows MIME types for many plugins.  If no explicit map exists,
    # preserve a safe original suffix and a best-effort MIME type.  The AI copy
    # is normalized later, so provider compatibility does not depend on this.
    suffix = _safe_original_suffix(original_filename)
    media_type = (
        Image.MIME.get(normalized)
        or mimetypes.guess_type(original_filename or "")[0]
        or "application/octet-stream"
    )
    return suffix, media_type


def _load_image(data: bytes):
    if not data:
        raise ReferenceImageError("The image file is empty.")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter(
                "error",
                Image.DecompressionBombWarning,
            )

            source = Image.open(BytesIO(data))

            # AI providers do not consume animation as a reference sequence.
            # Use the first frame deterministically for GIF/TIFF/other
            # multi-frame image containers.
            try:
                source.seek(0)
            except EOFError:
                pass

            source.load()

            # Detach from the in-memory file before returning.
            image = source.copy()
            image_format = source.format
            source.close()

    except Image.DecompressionBombError as error:
        raise ReferenceImageError(
            "The image dimensions are too large to process safely."
        ) from error
    except Image.DecompressionBombWarning as error:
        raise ReferenceImageError(
            "The image dimensions are too large to process safely."
        ) from error
    except UnidentifiedImageError as error:
        hint = (
            " HEIC/HEIF files require the pillow-heif package."
            if not _HEIF_ENABLED
            else ""
        )
        raise ReferenceImageError(
            "Hyperex could not decode this image file."
            + hint
        ) from error
    except Exception as error:
        raise ReferenceImageError(
            "Hyperex could not safely decode this image file: "
            f"{str(error)[:240]}"
        ) from error

    if image.width < 1 or image.height < 1:
        raise ReferenceImageError(
            "The image has invalid dimensions."
        )

    return image, image_format


def inspect_reference_image(
    data: bytes,
    original_filename: str | None = None,
) -> dict:
    """Fully decode an upload and return its actual type/dimensions.

    This deliberately does not trust the file extension or browser MIME type.
    A .jpg containing PNG bytes (or vice versa) is handled from its real data.
    """

    image, image_format = _load_image(data)

    try:
        extension, media_type = _format_details(
            image_format,
            original_filename,
        )

        return {
            "extension": extension,
            "media_type": media_type,
            "format": image_format or "unknown",
            "width": int(image.width),
            "height": int(image.height),
            "mode": str(image.mode),
        }
    finally:
        image.close()


def _has_alpha(image: Image.Image) -> bool:
    return (
        "A" in image.getbands()
        or "transparency" in image.info
    )


def _encode_rgb_jpeg(image: Image.Image) -> bytes:
    rgb = image.convert("RGB")

    try:
        # Start visually lossless for reference use.  If an unusually large
        # decoded image expands beyond the existing 20 MB reference limit,
        # lower JPEG quality without resizing/cropping the source.
        for quality in (95, 92, 88, 84, 80):
            output = BytesIO()
            rgb.save(
                output,
                format="JPEG",
                quality=quality,
                subsampling=0,
            )
            payload = output.getvalue()

            if len(payload) <= MAX_AI_REFERENCE_BYTES:
                return payload

    finally:
        rgb.close()

    raise ReferenceImageError(
        "The decoded image is too large to prepare for the AI provider. "
        "Please use a smaller-resolution reference image."
    )


def normalize_reference_image(
    data: bytes,
    original_filename: str | None = None,
) -> dict:
    """Return a provider-safe JPEG/PNG payload decoded from arbitrary raster input."""

    image, source_format = _load_image(data)

    try:
        try:
            oriented = ImageOps.exif_transpose(image)
        except Exception:
            oriented = image.copy()

        try:
            if _has_alpha(oriented):
                rgba = oriented.convert("RGBA")
                try:
                    output = BytesIO()
                    rgba.save(
                        output,
                        format="PNG",
                        compress_level=6,
                    )
                    payload = output.getvalue()
                finally:
                    rgba.close()

                if len(payload) <= MAX_AI_REFERENCE_BYTES:
                    return {
                        "data": payload,
                        "extension": ".png",
                        "media_type": "image/png",
                        "source_format": source_format or "unknown",
                    }

                # Extremely large alpha images can inflate dramatically as PNG.
                # Flatten only as a last-resort compatibility path instead of
                # resizing the reference and losing geometry/detail.
                canvas = Image.new(
                    "RGB",
                    oriented.size,
                    (255, 255, 255),
                )
                alpha_source = oriented.convert("RGBA")
                try:
                    canvas.paste(
                        alpha_source,
                        mask=alpha_source.getchannel("A"),
                    )
                    payload = _encode_rgb_jpeg(canvas)
                finally:
                    alpha_source.close()
                    canvas.close()

                return {
                    "data": payload,
                    "extension": ".jpg",
                    "media_type": "image/jpeg",
                    "source_format": source_format or "unknown",
                }

            payload = _encode_rgb_jpeg(oriented)

            return {
                "data": payload,
                "extension": ".jpg",
                "media_type": "image/jpeg",
                "source_format": source_format or "unknown",
            }
        finally:
            if oriented is not image:
                oriented.close()
    finally:
        image.close()


def prepare_job_references_for_ai(job: dict) -> dict:
    """Attach provider-safe payloads to every job reference once.

    New Hyperex uploads are normalized before storage and marked with a
    ``_normalized`` stored filename.  Those can be reused byte-for-byte.  Older
    jobs are normalized here on demand, which makes this fix backward-compatible
    with references created before the normalization layer existed.

    The prepared job object is shared by concurrent image workers, so a legacy
    reference is decoded/re-encoded only once per batch rather than once per
    generated output.
    """

    for reference in job.get("references", []):
        if reference.get("ai_data") is not None:
            continue

        raw_data = reference.get("data")
        if raw_data is None:
            absolute_path = reference.get("absolute_path")
            if absolute_path is None:
                raise ReferenceImageError(
                    f"Reference Image {reference.get('position', '?')} is unavailable."
                )
            raw_data = absolute_path.read_bytes()

        stored_filename = str(reference.get("stored_filename") or "")
        provider_safe = bool(reference.get("provider_safe")) or (
            "_normalized" in Path(stored_filename).stem
        )

        if provider_safe:
            suffix = Path(stored_filename).suffix.lower()
            if suffix in {".jpg", ".jpeg"}:
                media_type = "image/jpeg"
                extension = ".jpg"
            elif suffix == ".png":
                media_type = "image/png"
                extension = ".png"
            else:
                # A marker with an unexpected extension should never happen,
                # but normalize again rather than trusting it.
                provider_safe = False

        if provider_safe:
            reference["ai_data"] = raw_data
            reference["ai_media_type"] = media_type
            reference["ai_extension"] = extension
            reference["ai_source_format"] = "hyperex-normalized"
            continue

        prepared = normalize_reference_image(
            raw_data,
            reference.get("original_filename"),
        )

        reference["ai_data"] = prepared["data"]
        reference["ai_media_type"] = prepared["media_type"]
        reference["ai_extension"] = prepared["extension"]
        reference["ai_source_format"] = prepared["source_format"]

    return job
