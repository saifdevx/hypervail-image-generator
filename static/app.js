const uploadZone = document.getElementById("uploadZone");
const imageInput = document.getElementById("imageInput");
const imagePreviewGrid = document.getElementById("imagePreviewGrid");

const description = document.getElementById("description");
const characterCount = document.getElementById("characterCount");

const summaryProfile = document.getElementById("summaryProfile");
const summaryImages = document.getElementById("summaryImages");
const summaryCount = document.getElementById("summaryCount");

const generateButton = document.getElementById("generateButton");
const toast = document.getElementById("toast");


let selectedImages = [];
let selectedCount = "auto";


/* ------------------------------
   PROFILE SELECTION
------------------------------ */

const profileCards =
    document.querySelectorAll(".profile-card");


profileCards.forEach(card => {

    card.addEventListener("click", () => {

        profileCards.forEach(item => {
            item.classList.remove("active-profile");
        });

        card.classList.add("active-profile");

        const radio =
            card.querySelector("input");

        radio.checked = true;

        summaryProfile.textContent =
            radio.value === "hero"
                ? "Hero Images"
                : "UGC Images";

    });

});


/* ------------------------------
   IMAGE UPLOAD
------------------------------ */

uploadZone.addEventListener("click", () => {
    imageInput.click();
});


imageInput.addEventListener("change", event => {
    addImages(event.target.files);
});


uploadZone.addEventListener("dragover", event => {

    event.preventDefault();

    uploadZone.classList.add("dragging");

});


uploadZone.addEventListener("dragleave", () => {

    uploadZone.classList.remove("dragging");

});


uploadZone.addEventListener("drop", event => {

    event.preventDefault();

    uploadZone.classList.remove("dragging");

    addImages(event.dataTransfer.files);

});


function addImages(files) {

    const imageFiles = Array.from(files)
        .filter(file => file.type.startsWith("image/"));


    for (const file of imageFiles) {

        if (selectedImages.length >= 4) {
            showToast("Maximum 4 reference images.");
            break;
        }

        selectedImages.push(file);

    }

    renderImages();

    imageInput.value = "";

}


function renderImages() {

    imagePreviewGrid.innerHTML = "";


    selectedImages.forEach((file, index) => {

        const preview =
            document.createElement("div");

        preview.className = "image-preview";


        const image =
            document.createElement("img");

        image.src =
            URL.createObjectURL(file);

        image.alt =
            `Reference ${index + 1}`;


        const number =
            document.createElement("span");

        number.className = "image-number";

        number.textContent =
            `Image ${index + 1}`;


        const remove =
            document.createElement("button");

        remove.className = "remove-image";

        remove.innerHTML = "×";


        remove.addEventListener("click", event => {

            event.stopPropagation();

            selectedImages.splice(index, 1);

            renderImages();

        });


        preview.appendChild(image);
        preview.appendChild(number);
        preview.appendChild(remove);

        imagePreviewGrid.appendChild(preview);

    });


    summaryImages.textContent =
        selectedImages.length;

}


/* ------------------------------
   DESCRIPTION COUNT
------------------------------ */

description.addEventListener("input", () => {

    characterCount.textContent =
        `${description.value.length} characters`;

});


/* ------------------------------
   OUTPUT COUNT
------------------------------ */

const countButtons =
    document.querySelectorAll(".count-button");


countButtons.forEach(button => {

    button.addEventListener("click", () => {

        countButtons.forEach(item => {
            item.classList.remove("selected");
        });


        button.classList.add("selected");

        selectedCount =
            button.dataset.count;


        summaryCount.textContent =
            selectedCount === "auto"
                ? "Auto"
                : selectedCount;

    });

});


/* ------------------------------
   GENERATE BUTTON
------------------------------ */

generateButton.addEventListener("click", () => {

    if (selectedImages.length === 0) {

        showToast(
            "Add at least one reference image first."
        );

        return;

    }


    showToast(
        "UI is ready. AI generation will be connected in a later step."
    );

});


/* ------------------------------
   TOAST
------------------------------ */

let toastTimer;


function showToast(message) {

    clearTimeout(toastTimer);

    toast.textContent = message;

    toast.classList.add("visible");


    toastTimer = setTimeout(() => {

        toast.classList.remove("visible");

    }, 3000);

}