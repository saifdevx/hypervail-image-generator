/* =========================================================
   IMAGE AGENT — STEP 11 STUDIO UI
========================================================= */

const $ = id =>
    document.getElementById(id);


/* =========================================================
   DOM
========================================================= */

const navGenerate = $("navGenerate");
const navProfiles = $("navProfiles");
const navHistory = $("navHistory");
const navSettings = $("navSettings");

const generateView = $("generateView");
const profilesView = $("profilesView");
const historyView = $("historyView");
const settingsView = $("settingsView");

const createPlannerSummary = $("createPlannerSummary");
const createImageSummary = $("createImageSummary");
const createCostEstimate = $("createCostEstimate");
const openSettingsFromCreate = $("openSettingsFromCreate");

const profileOptions = $("profileOptions");

const imageInput = $("imageInput");
const replaceImageInput = $("replaceImageInput");
const uploadZone = $("uploadZone");
const imagePreviewGrid = $("imagePreviewGrid");

const description = $("description");
const characterCount = $("characterCount");

const autoGenerateImages = $("autoGenerateImages");

const generateButton = $("generateButton");
const generateButtonLabel = $("generateButtonLabel");
const generateButtonArrow = $("generateButtonArrow");

const pipelineSection = $("pipelineSection");
const pipelineJobId = $("pipelineJobId");
const pipelineReferences = $("pipelineReferences");
const pipelinePlanner = $("pipelinePlanner");
const pipelineVerify = $("pipelineVerify");
const pipelineImages = $("pipelineImages");

const imageBatchSection = $("imageBatchSection");
const imageBatchCount = $("imageBatchCount");
const imageBatchProgressBar = $("imageBatchProgressBar");
const imageBatchProgressText = $("imageBatchProgressText");
const imageBatchFailureText = $("imageBatchFailureText");
const imageBatchGrid = $("imageBatchGrid");
const retryIncompleteImagesButton = $("retryIncompleteImagesButton");
const refreshImageBatchButton = $("refreshImageBatchButton");

const resultsSection = $("resultsSection");
const resultsSubtitle = $("resultsSubtitle");
const resultsGrid = $("resultsGrid");
const compareSelectedButton = $("compareSelectedButton");
const downloadAllButton = $("downloadAllButton");

const advancedPipelineToggle = $("advancedPipelineToggle");
const advancedToggleState = $("advancedToggleState");
const advancedContent = $("advancedContent");

const plannerResultSection = $("plannerResultSection");
const plannerResultModel = $("plannerResultModel");
const plannerRawOutput = $("plannerRawOutput");
const copyPlannerOutputButton = $("copyPlannerOutputButton");
const retryPlannerButton = $("retryPlannerButton");

const promptPackagesSection = $("promptPackagesSection");
const promptPackagesCount = $("promptPackagesCount");
const sharedNegativeBox = $("sharedNegativeBox");
const sharedNegativeText = $("sharedNegativeText");
const promptPackageGrid = $("promptPackageGrid");
const generateAllImagesButton = $("generateAllImagesButton");

const jobPanelStatus = $("jobPanelStatus");
const jobEmptyState = $("jobEmptyState");
const jobSavedState = $("jobSavedState");
const currentJobId = $("currentJobId");
const storedReferenceGrid = $("storedReferenceGrid");

const summaryProfile = $("summaryProfile");
const summaryPlanner = $("summaryPlanner");
const summaryImageEngine = $("summaryImageEngine");
const summaryImages = $("summaryImages");
const summaryCount = $("summaryCount");
const summaryVersion = $("summaryVersion");

const historyCountLabel = $("historyCountLabel");
const historySearchInput = $("historySearchInput");
const historyProfileFilter = $("historyProfileFilter");
const historyStatusFilter = $("historyStatusFilter");
const historyPlannerFilter = $("historyPlannerFilter");
const historyImageProviderFilter = $("historyImageProviderFilter");
const historyFavoritesOnly = $("historyFavoritesOnly");
const historyClearFiltersButton = $("historyClearFiltersButton");
const historyGrid = $("historyGrid");
const historyEmptyState = $("historyEmptyState");
const historyEmptyCreateButton = $("historyEmptyCreateButton");


/* Profiles */

const newProfileButton = $("newProfileButton");
const libraryCount = $("libraryCount");
const profileSearch = $("profileSearch");
const profileManagerList = $("profileManagerList");

const profileEditorEmpty = $("profileEditorEmpty");
const profileEditorContent = $("profileEditorContent");
const profileEditorTitle = $("profileEditorTitle");
const profileStateBadge = $("profileStateBadge");

const profileNameInput = $("profileNameInput");
const profileDescriptionInput = $("profileDescriptionInput");
const profileInstructionEditor = $("profileInstructionEditor");
const instructionCharacterCount = $("instructionCharacterCount");

const saveDetailsButton = $("saveDetailsButton");
const saveVersionButton = $("saveVersionButton");
const archiveProfileButton = $("archiveProfileButton");
const restoreProfileButton = $("restoreProfileButton");
const deleteProfileButton = $("deleteProfileButton");


/* Settings */

const saveSettingsButton = $("saveSettingsButton");

const plannerProviderStatus = $("plannerProviderStatus");
const plannerProviderSelect = $("plannerProviderSelect");
const plannerModelSelect = $("plannerModelSelect");
const openaiReasoningField = $("openaiReasoningField");
const openaiReasoningSelect = $("openaiReasoningSelect");
const plannerConnectionSummary = $("plannerConnectionSummary");
const testPlannerButton = $("testPlannerButton");
const plannerTestResult = $("plannerTestResult");

const imageProviderStatus = $("imageProviderStatus");
const imageProviderSelect = $("imageProviderSelect");
const imageModelSelect = $("imageModelSelect");
const openaiQualityField = $("openaiQualityField");
const openaiQualitySelect = $("openaiQualitySelect");
const imageSizeSelect = $("imageSizeSelect");
const geminiAspectField = $("geminiAspectField");
const geminiAspectSelect = $("geminiAspectSelect");
const batchConcurrencySelect = $("batchConcurrencySelect");
const imageConnectionSummary = $("imageConnectionSummary");
const testImageProviderButton = $("testImageProviderButton");
const imageTestResult = $("imageTestResult");

const openaiConnectedBadge = $("openaiConnectedBadge");
const geminiConnectedBadge = $("geminiConnectedBadge");


/* New Profile Modal */

const newProfileModal = $("newProfileModal");
const modalCloseButton = $("modalCloseButton");
const cancelCreateProfile = $("cancelCreateProfile");
const newProfileForm = $("newProfileForm");
const newProfileName = $("newProfileName");
const newProfileDescription = $("newProfileDescription");
const newProfileInstruction = $("newProfileInstruction");
const newInstructionCharacterCount = $("newInstructionCharacterCount");


/* Prompt Modal */

const finalInputModal = $("finalInputModal");
const closeFinalInputModal = $("closeFinalInputModal");
const finalInputTitle = $("finalInputTitle");
const finalInputStrategy = $("finalInputStrategy");
const finalInputPreview = $("finalInputPreview");
const copyFinalInputModalButton = $("copyFinalInputModalButton");


/* Image Preview */

const imagePreviewModal = $("imagePreviewModal");
const closeImagePreviewModal = $("closeImagePreviewModal");
const previewImagePosition = $("previewImagePosition");
const previewImageTitle = $("previewImageTitle");
const previewLargeImage = $("previewLargeImage");
const previewPreviousButton = $("previewPreviousButton");
const previewNextButton = $("previewNextButton");
const previewProviderMeta = $("previewProviderMeta");
const previewPromptButton = $("previewPromptButton");
const previewRegenerateButton = $("previewRegenerateButton");
const previewDownloadButton = $("previewDownloadButton");


/* Regenerate */

const regenerateModal = $("regenerateModal");
const closeRegenerateModal = $("closeRegenerateModal");
const cancelRegenerateButton = $("cancelRegenerateButton");
const confirmRegenerateButton = $("confirmRegenerateButton");
const regenerateTitle = $("regenerateTitle");
const regenerateDirection = $("regenerateDirection");


/* Compare */

const compareModal = $("compareModal");
const closeCompareModal = $("closeCompareModal");
const compareImageA = $("compareImageA");
const compareImageB = $("compareImageB");
const compareTitleA = $("compareTitleA");
const compareTitleB = $("compareTitleB");


/* History Detail */

const historyDetailModal = $("historyDetailModal");
const closeHistoryDetailModal = $("closeHistoryDetailModal");
const historyDetailKicker = $("historyDetailKicker");
const historyDetailTitle = $("historyDetailTitle");
const historyDetailMeta = $("historyDetailMeta");
const historyDetailFavoriteButton = $("historyDetailFavoriteButton");
const historyDuplicateButton = $("historyDuplicateButton");
const historyDownloadAllButton = $("historyDownloadAllButton");
const historyDetailWorkflow = $("historyDetailWorkflow");
const historyDetailPlanner = $("historyDetailPlanner");
const historyDetailImageEngine = $("historyDetailImageEngine");
const historyDetailOutputs = $("historyDetailOutputs");
const historyDetailReferenceCount = $("historyDetailReferenceCount");
const historyDetailReferences = $("historyDetailReferences");
const historyDetailDirection = $("historyDetailDirection");
const historyDetailImageCount = $("historyDetailImageCount");
const historyDetailImages = $("historyDetailImages");
const historyDetailPrompts = $("historyDetailPrompts");

const toast = $("toast");


/* =========================================================
   STATE
========================================================= */

let profiles = [];
let managerProfiles = [];

let selectedProfileId = null;
let selectedProfileVersionId = null;

let selectedImages = [];
let replaceTargetIndex = null;
let draggedReferenceIndex = null;

let selectedCount = "auto";

let editingProfileId = null;
let editingProfileName = null;

let currentJob = null;
let currentPromptPackages = [];
let activeFinalPackage = null;

let settingsPayload = null;

let imageBatchPollTimer = null;
let imageBatchRequestRunning = false;

let previewResults = [];
let previewIndex = 0;
let previewPackageLookup = [];
let previewJobId = null;

let lastRenderedBatch = null;
let selectedCompareIds = new Set();

let historyItems = [];
let historyOptions = null;
let historyDetail = null;
let historySearchTimer = null;

let regenerateTarget = null;
let regenerateJobId = null;

let advancedOpen = false;

let toastTimer = null;


/* =========================================================
   VIEW NAVIGATION
========================================================= */

function showView(
    view
) {
    const mapping = {
        generate:
            generateView,
        profiles:
            profilesView,
        history:
            historyView,
        settings:
            settingsView,
    };

    Object.entries(
        mapping
    ).forEach(
        ([name, element]) => {
            element.classList.toggle(
                "hidden-view",
                name !== view
            );
        }
    );

    navGenerate.classList.toggle(
        "active",
        view === "generate"
    );

    navProfiles.classList.toggle(
        "active",
        view === "profiles"
    );

    navHistory.classList.toggle(
        "active",
        view === "history"
    );

    navSettings.classList.toggle(
        "active",
        view === "settings"
    );
}


navGenerate.addEventListener(
    "click",
    () => {
        showView(
            "generate"
        );
    }
);


navProfiles.addEventListener(
    "click",
    async () => {
        showView(
            "profiles"
        );

        await loadManagerProfiles();

        const preferred =
            editingProfileId
            ??
            selectedProfileId
            ??
            managerProfiles[0]?.id;

        if (preferred) {
            await openProfileEditor(
                preferred
            );
        }
    }
);


navHistory.addEventListener(
    "click",
    async () => {
        showView(
            "history"
        );

        await ensureHistoryOptions();
        await loadHistory();
    }
);


navSettings.addEventListener(
    "click",
    async () => {
        showView(
            "settings"
        );

        await loadSettings();
    }
);


openSettingsFromCreate.addEventListener(
    "click",
    async () => {
        showView(
            "settings"
        );

        await loadSettings();
    }
);


/* =========================================================
   API HELPERS
========================================================= */

async function apiError(
    response
) {
    try {
        const data =
            await response.json();

        if (
            typeof data.detail
            ===
            "string"
        ) {
            return friendlyError(
                data.detail
            );
        }

        if (
            Array.isArray(
                data.detail
            )
        ) {
            return data.detail
                .map(
                    item =>
                        item.msg
                        ||
                        String(item)
                )
                .join(
                    " · "
                );
        }
    } catch {
        // Ignore JSON parse failure.
    }

    return (
        `Request failed (${response.status}).`
    );
}


function friendlyError(
    message
) {
    const lower =
        String(
            message
            ||
            ""
        ).toLowerCase();

    if (
        lower.includes(
            "resource_exhausted"
        )
        ||
        lower.includes(
            "quota"
        )
        ||
        lower.includes(
            "rate limit"
        )
    ) {
        return (
            "Provider quota or credit limit reached. "
            +
            "Check the selected provider's billing/rate limits."
        );
    }

    if (
        lower.includes(
            "401"
        )
        ||
        lower.includes(
            "unauthenticated"
        )
        ||
        lower.includes(
            "invalid api key"
        )
    ) {
        return (
            "Provider authentication failed. "
            +
            "Check the API key saved in .env."
        );
    }

    if (
        lower.includes(
            "503"
        )
        ||
        lower.includes(
            "high demand"
        )
        ||
        lower.includes(
            "unavailable"
        )
    ) {
        return (
            "The provider is temporarily busy. "
            +
            "Retry in a moment."
        );
    }

    return message;
}


async function copyText(
    value
) {
    try {
        await navigator.clipboard.writeText(
            value
        );

        showToast(
            "Copied."
        );
    } catch {
        showToast(
            "Could not access clipboard."
        );
    }
}


/* =========================================================
   SETTINGS
========================================================= */

async function loadSettings() {
    try {
        const response =
            await fetch(
                "/api/settings"
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        settingsPayload =
            await response.json();

        renderSettings();
        renderCreateProviderSummary();

    } catch (error) {
        console.error(
            error
        );

        showToast(
            error.message
        );
    }
}


function fillSelect(
    element,
    items,
    selectedValue
) {
    element.innerHTML =
        "";

    items.forEach(
        item => {
            const option =
                document.createElement(
                    "option"
                );

            if (
                typeof item
                ===
                "object"
            ) {
                option.value =
                    item.id;

                option.textContent =
                    item.note
                        ?
                        `${item.label} — ${item.note}`
                        :
                        item.label;
            } else {
                option.value =
                    String(item);

                option.textContent =
                    String(item);
            }

            option.selected =
                String(
                    option.value
                )
                ===
                String(
                    selectedValue
                );

            element.appendChild(
                option
            );
        }
    );
}


function renderSettings() {
    if (!settingsPayload) {
        return;
    }

    const settings =
        settingsPayload.settings;

    const catalog =
        settingsPayload.catalog;

    fillSelect(
        plannerProviderSelect,
        catalog.planner_providers,
        settings.planner_provider
    );

    renderPlannerModelOptions();

    fillSelect(
        openaiReasoningSelect,
        catalog.openai_reasoning,
        settings.openai_planner_reasoning
    );

    fillSelect(
        imageProviderSelect,
        catalog.image_providers,
        settings.image_provider
    );

    renderImageProviderOptions();

    fillSelect(
        batchConcurrencySelect,
        catalog.batch_concurrency,
        settings.batch_concurrency
    );

    autoGenerateImages.checked =
        Boolean(
            settings.auto_generate_images
        );

    renderConnectionBadges();

    renderPlannerSettingsState();
    renderImageSettingsState();
}


function renderPlannerModelOptions() {
    if (!settingsPayload) {
        return;
    }

    const provider =
        plannerProviderSelect.value
        ||
        settingsPayload.settings
            .planner_provider;

    const settings =
        settingsPayload.settings;

    const selected =
        provider === "gemini"
            ?
            settings.gemini_planner_model
            :
            settings.openai_planner_model;

    fillSelect(
        plannerModelSelect,
        settingsPayload.catalog
            .planner_models[
                provider
            ],
        selected
    );

    openaiReasoningField
        .classList
        .toggle(
            "hidden-element",
            provider !== "openai"
        );
}


function renderImageProviderOptions() {
    if (!settingsPayload) {
        return;
    }

    const provider =
        imageProviderSelect.value
        ||
        settingsPayload.settings
            .image_provider;

    const settings =
        settingsPayload.settings;

    const model =
        provider === "openai"
            ?
            settings.openai_image_model
            :
            settings.gemini_image_model;

    fillSelect(
        imageModelSelect,
        settingsPayload.catalog
            .image_models[
                provider
            ],
        model
    );

    if (
        provider
        ===
        "openai"
    ) {
        fillSelect(
            openaiQualitySelect,
            settingsPayload.catalog
                .openai_image_quality,
            settings.openai_image_quality
        );

        fillSelect(
            imageSizeSelect,
            settingsPayload.catalog
                .openai_image_sizes,
            settings.openai_image_size
        );
    } else {
        fillSelect(
            imageSizeSelect,
            settingsPayload.catalog
                .gemini_image_sizes,
            settings.gemini_image_size
        );

        fillSelect(
            geminiAspectSelect,
            settingsPayload.catalog
                .gemini_image_aspect_ratios,
            settings
                .gemini_image_aspect_ratio
        );
    }

    openaiQualityField
        .classList
        .toggle(
            "hidden-element",
            provider !== "openai"
        );

    geminiAspectField
        .classList
        .toggle(
            "hidden-element",
            provider !== "gemini"
        );

    // Flash Lite image only supports 1K.
    if (
        provider === "gemini"
        &&
        imageModelSelect.value
        ===
        "gemini-3.1-flash-lite-image"
    ) {
        imageSizeSelect.value =
            "1K";

        imageSizeSelect.disabled =
            true;
    } else {
        imageSizeSelect.disabled =
            false;
    }
}


function renderConnectionBadges() {
    const planner =
        settingsPayload?.planner;

    const image =
        settingsPayload?.image;

    const openaiConfigured =
        Boolean(
            planner?.providers?.openai
                ?.configured
            ||
            image?.providers?.openai
                ?.configured
        );

    const geminiConfigured =
        Boolean(
            planner?.providers?.gemini
                ?.configured
            ||
            image?.providers?.gemini
                ?.configured
        );

    setConnectionBadge(
        openaiConnectedBadge,
        openaiConfigured
    );

    setConnectionBadge(
        geminiConnectedBadge,
        geminiConfigured
    );
}


function setConnectionBadge(
    element,
    connected
) {
    element.textContent =
        connected
            ?
            "CONNECTED"
            :
            "NOT CONFIGURED";

    element.classList.toggle(
        "connected",
        connected
    );

    element.classList.toggle(
        "not-connected",
        !connected
    );
}


function renderPlannerSettingsState() {
    const provider =
        plannerProviderSelect.value;

    const providerStatus =
        settingsPayload
            ?.planner
            ?.providers
            ?.[
                provider
            ];

    const configured =
        Boolean(
            providerStatus
                ?.configured
        );

    plannerProviderStatus.textContent =
        configured
            ?
            "READY"
            :
            "NEEDS KEY";

    plannerProviderStatus
        .classList
        .toggle(
            "ready",
            configured
        );

    plannerProviderStatus
        .classList
        .toggle(
            "warning",
            !configured
        );

    plannerConnectionSummary.textContent =
        configured
            ?
            `${provider.toUpperCase()} credential is configured.`
            :
            `${provider.toUpperCase()} key is missing from .env.`;
}


function renderImageSettingsState() {
    const provider =
        imageProviderSelect.value;

    const providerStatus =
        settingsPayload
            ?.image
            ?.providers
            ?.[
                provider
            ];

    const configured =
        Boolean(
            providerStatus
                ?.configured
        );

    imageProviderStatus.textContent =
        configured
            ?
            "READY"
            :
            "NEEDS KEY";

    imageProviderStatus
        .classList
        .toggle(
            "ready",
            configured
        );

    imageProviderStatus
        .classList
        .toggle(
            "warning",
            !configured
        );

    imageConnectionSummary.textContent =
        configured
            ?
            `${provider.toUpperCase()} credential is configured.`
            :
            `${provider.toUpperCase()} key is missing from .env.`;
}


plannerProviderSelect.addEventListener(
    "change",
    () => {
        renderPlannerModelOptions();
        renderPlannerSettingsState();
    }
);


imageProviderSelect.addEventListener(
    "change",
    () => {
        renderImageProviderOptions();
        renderImageSettingsState();
        updateCreateCostEstimate();
    }
);


imageModelSelect.addEventListener(
    "change",
    () => {
        renderImageProviderOptions();
        updateCreateCostEstimate();
    }
);


openaiQualitySelect.addEventListener(
    "change",
    updateCreateCostEstimate
);


imageSizeSelect.addEventListener(
    "change",
    updateCreateCostEstimate
);


async function saveSettings() {
    if (!settingsPayload) {
        return;
    }

    const providerPlanner =
        plannerProviderSelect.value;

    const providerImage =
        imageProviderSelect.value;

    const body = {
        planner_provider:
            providerPlanner,

        openai_planner_reasoning:
            openaiReasoningSelect.value,

        image_provider:
            providerImage,

        batch_concurrency:
            Number(
                batchConcurrencySelect
                    .value
            ),

        auto_generate_images:
            autoGenerateImages.checked,
    };

    if (
        providerPlanner
        ===
        "gemini"
    ) {
        body.gemini_planner_model =
            plannerModelSelect.value;
    } else {
        body.openai_planner_model =
            plannerModelSelect.value;
    }

    if (
        providerImage
        ===
        "openai"
    ) {
        body.openai_image_model =
            imageModelSelect.value;

        body.openai_image_quality =
            openaiQualitySelect.value;

        body.openai_image_size =
            imageSizeSelect.value;
    } else {
        body.gemini_image_model =
            imageModelSelect.value;

        body.gemini_image_size =
            imageSizeSelect.value;

        body.gemini_image_aspect_ratio =
            geminiAspectSelect.value;
    }

    saveSettingsButton.disabled =
        true;

    saveSettingsButton.textContent =
        "Saving…";

    try {
        const response =
            await fetch(
                "/api/settings",
                {
                    method:
                        "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            body
                        ),
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const updated =
            await response.json();

        // Refresh the full catalog/status payload.
        await loadSettings();

        showToast(
            "Provider settings saved. No restart required."
        );

    } catch (error) {
        console.error(
            error
        );

        showToast(
            error.message
        );

    } finally {
        saveSettingsButton.disabled =
            false;

        saveSettingsButton.textContent =
            "Save settings";
    }
}


saveSettingsButton.addEventListener(
    "click",
    saveSettings
);


testPlannerButton.addEventListener(
    "click",
    async () => {
        plannerTestResult.className =
            "connection-result";

        plannerTestResult.textContent =
            "Testing selected planner…";

        testPlannerButton.disabled =
            true;

        try {
            // Save selection first so the backend tests exactly
            // what the user currently sees.
            await saveSettings();

            const response =
                await fetch(
                    "/api/providers/planner/test",
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            const result =
                await response.json();

            plannerTestResult.classList.add(
                "success"
            );

            plannerTestResult.textContent =
                `Connected: ${result.provider || plannerProviderSelect.value} · ${result.model || plannerModelSelect.value}`;

        } catch (error) {
            plannerTestResult.classList.add(
                "error"
            );

            plannerTestResult.textContent =
                error.message;

        } finally {
            testPlannerButton.disabled =
                false;
        }
    }
);


testImageProviderButton.addEventListener(
    "click",
    async () => {
        imageTestResult.className =
            "connection-result";

        imageTestResult.textContent =
            "Testing selected image provider credential…";

        testImageProviderButton.disabled =
            true;

        try {
            await saveSettings();

            const provider =
                imageProviderSelect.value;

            const endpoint =
                provider === "openai"
                    ?
                    "/api/providers/openai/test"
                    :
                    "/api/providers/gemini/test";

            const response =
                await fetch(
                    endpoint,
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            imageTestResult.classList.add(
                "success"
            );

            imageTestResult.textContent =
                `${provider.toUpperCase()} credential connected.`;

        } catch (error) {
            imageTestResult.classList.add(
                "error"
            );

            imageTestResult.textContent =
                error.message;

        } finally {
            testImageProviderButton.disabled =
                false;
        }
    }
);


/* =========================================================
   CREATE PROVIDER SUMMARY / COST
========================================================= */

function renderCreateProviderSummary() {
    if (!settingsPayload) {
        return;
    }

    const settings =
        settingsPayload.settings;

    const plannerProvider =
        settings.planner_provider;

    const plannerModel =
        plannerProvider
        ===
        "gemini"
            ?
            settings
                .gemini_planner_model
            :
            settings
                .openai_planner_model;

    createPlannerSummary.textContent =
        `${plannerProvider === "gemini" ? "Gemini" : "OpenAI"} · ${plannerModel}`;

    const imageProvider =
        settings.image_provider;

    const imageModel =
        imageProvider
        ===
        "openai"
            ?
            settings
                .openai_image_model
            :
            settings
                .gemini_image_model;

    const quality =
        imageProvider
        ===
        "openai"
            ?
            ` · ${capitalize(settings.openai_image_quality)}`
            :
            "";

    createImageSummary.textContent =
        `${imageProvider === "gemini" ? "Gemini" : "OpenAI"} · ${imageModel}${quality}`;

    summaryPlanner.textContent =
        `${plannerProvider === "gemini" ? "Gemini" : "OpenAI"} · ${plannerModel}`;

    summaryImageEngine.textContent =
        `${imageProvider === "gemini" ? "Gemini" : "OpenAI"} · ${imageModel}`;

    updateCreateCostEstimate();
}


function updateCreateCostEstimate() {
    if (!settingsPayload) {
        createCostEstimate.textContent =
            "—";

        return;
    }

    const settings =
        settingsPayload.settings;

    const count =
        selectedCount === "auto"
            ?
            null
            :
            Number(
                selectedCount
            );

    if (
        settings.image_provider
        ===
        "openai"
    ) {
        createCostEstimate.textContent =
            count
                ?
                `${count} images · ${capitalize(settings.openai_image_quality)}`
                :
                `${capitalize(settings.openai_image_quality)} · provider billed`;

        return;
    }

    const model =
        settings.gemini_image_model;

    const size =
        settings.gemini_image_size;

    let perImage = null;

    if (
        model
        ===
        "gemini-3.1-flash-lite-image"
        &&
        size === "1K"
    ) {
        perImage = 0.0336;
    }

    if (
        model
        ===
        "gemini-3.1-flash-image"
    ) {
        perImage = {
            "1K": 0.067,
            "2K": 0.101,
            "4K": 0.151,
        }[
            size
        ];
    }

    if (
        count
        &&
        perImage
    ) {
        createCostEstimate.textContent =
            `≈ $${(
                count
                *
                perImage
            ).toFixed(2)}`;
    } else {
        createCostEstimate.textContent =
            `${size} · provider billed`;
    }
}


/* =========================================================
   GENERATION PROFILES
========================================================= */

async function loadProfiles(
    preferredId =
        selectedProfileId
) {
    profileOptions.innerHTML = `
        <div class="loading-state">
            Loading profiles…
        </div>
    `;

    try {
        const response =
            await fetch(
                "/api/profiles"
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const data =
            await response.json();

        profiles =
            Array.isArray(
                data.profiles
            )
                ?
                data.profiles
                :
                [];

        renderGenerateProfiles(
            preferredId
        );

    } catch (error) {
        profileOptions.innerHTML = `
            <div class="loading-state">
                Could not load profiles.
            </div>
        `;

        showToast(
            error.message
        );
    }
}


function renderGenerateProfiles(
    preferredId
) {
    profileOptions.innerHTML =
        "";

    if (!profiles.length) {
        profileOptions.innerHTML = `
            <div class="loading-state">
                No active profiles. Create one in Profiles.
            </div>
        `;

        selectedProfileId =
            null;

        summaryProfile.textContent =
            "No workflow";

        return;
    }

    profiles.forEach(
        profile => {
            profileOptions.appendChild(
                createGenerateProfileCard(
                    profile
                )
            );
        }
    );

    let selected =
        profiles.find(
            item =>
                Number(item.id)
                ===
                Number(preferredId)
        );

    if (!selected) {
        selected =
            profiles[0];
    }

    selectGenerateProfile(
        selected.id
    );
}


function createGenerateProfileCard(
    profile
) {
    const card =
        document.createElement(
            "label"
        );

    card.className =
        "profile-card";

    card.dataset.profileId =
        String(
            profile.id
        );

    const input =
        document.createElement(
            "input"
        );

    input.type =
        "radio";

    input.name =
        "generation-profile";

    const icon =
        document.createElement(
            "div"
        );

    icon.className =
        "profile-icon";

    icon.textContent =
        initials(
            profile.name
        );

    const text =
        document.createElement(
            "div"
        );

    text.className =
        "profile-text";

    const title =
        document.createElement(
            "strong"
        );

    title.textContent =
        profile.name;

    const desc =
        document.createElement(
            "span"
        );

    desc.textContent =
        profile.description
        ||
        "Custom image-generation workflow";

    const check =
        document.createElement(
            "span"
        );

    check.className =
        "profile-check";

    check.textContent =
        "●";

    text.append(
        title,
        desc
    );

    card.append(
        input,
        icon,
        text,
        check
    );

    card.addEventListener(
        "click",
        () => {
            selectGenerateProfile(
                profile.id
            );
        }
    );

    return card;
}


function selectGenerateProfile(
    profileId
) {
    const profile =
        profiles.find(
            item =>
                Number(item.id)
                ===
                Number(profileId)
        );

    if (!profile) {
        return;
    }

    selectedProfileId =
        Number(
            profile.id
        );

    selectedProfileVersionId =
        Number(
            profile.active_version_id
            ||
            profile.version_id
            ||
            0
        );

    document
        .querySelectorAll(
            ".profile-card"
        )
        .forEach(
            card => {
                card.classList.toggle(
                    "active-profile",
                    Number(
                        card.dataset.profileId
                    )
                    ===
                    selectedProfileId
                );
            }
        );

    summaryProfile.textContent =
        profile.name;

    summaryVersion.textContent =
        profile.active_version_number
            ?
            `v${profile.active_version_number}`
            :
            "current";
}


/* =========================================================
   REFERENCE IMAGES
========================================================= */

uploadZone.addEventListener(
    "click",
    () => {
        imageInput.click();
    }
);


uploadZone.addEventListener(
    "dragover",
    event => {
        event.preventDefault();

        uploadZone.style.borderColor =
            "var(--orange)";
    }
);


uploadZone.addEventListener(
    "dragleave",
    () => {
        uploadZone.style.borderColor =
            "";
    }
);


uploadZone.addEventListener(
    "drop",
    event => {
        event.preventDefault();

        uploadZone.style.borderColor =
            "";

        addImages(
            event.dataTransfer.files
        );
    }
);


imageInput.addEventListener(
    "change",
    event => {
        addImages(
            event.target.files
        );

        imageInput.value =
            "";
    }
);


replaceImageInput.addEventListener(
    "change",
    event => {
        const file =
            event.target.files?.[0];

        if (
            file
            &&
            replaceTargetIndex
            !==
            null
        ) {
            if (
                !file.type.startsWith(
                    "image/"
                )
            ) {
                showToast(
                    "Choose an image file."
                );
            } else {
                selectedImages[
                    replaceTargetIndex
                ] = file;

                renderReferenceCards();
            }
        }

        replaceTargetIndex =
            null;

        replaceImageInput.value =
            "";
    }
);


function addImages(
    files
) {
    const imageFiles =
        Array.from(
            files
        ).filter(
            file =>
                file.type.startsWith(
                    "image/"
                )
        );

    for (
        const file
        of imageFiles
    ) {
        if (
            selectedImages.length
            >=
            4
        ) {
            showToast(
                "Maximum 4 reference images."
            );

            break;
        }

        selectedImages.push(
            file
        );
    }

    renderReferenceCards();
}


function renderReferenceCards() {
    imagePreviewGrid.innerHTML =
        "";

    selectedImages.forEach(
        (
            file,
            index
        ) => {
            const card =
                document.createElement(
                    "article"
                );

            card.className =
                "reference-card";

            card.draggable =
                true;

            card.dataset.index =
                String(index);

            const image =
                document.createElement(
                    "img"
                );

            const url =
                URL.createObjectURL(
                    file
                );

            image.src =
                url;

            image.alt =
                `Reference ${index + 1}`;

            image.onload =
                () =>
                    URL.revokeObjectURL(
                        url
                    );

            const badges =
                document.createElement(
                    "div"
                );

            badges.className =
                "reference-badges";

            const number =
                document.createElement(
                    "span"
                );

            number.className =
                "reference-badge";

            number.textContent =
                `IMAGE ${index + 1}`;

            badges.appendChild(
                number
            );

            if (index === 0) {
                const primary =
                    document.createElement(
                        "span"
                    );

                primary.className =
                    "reference-badge primary";

                primary.textContent =
                    "PRIMARY";

                badges.appendChild(
                    primary
                );
            }

            const footer =
                document.createElement(
                    "div"
                );

            footer.className =
                "reference-card-footer";

            const replace =
                document.createElement(
                    "button"
                );

            replace.type =
                "button";

            replace.textContent =
                "Replace";

            replace.addEventListener(
                "click",
                event => {
                    event.stopPropagation();

                    replaceTargetIndex =
                        index;

                    replaceImageInput.click();
                }
            );

            const remove =
                document.createElement(
                    "button"
                );

            remove.type =
                "button";

            remove.textContent =
                "Remove";

            remove.addEventListener(
                "click",
                event => {
                    event.stopPropagation();

                    selectedImages.splice(
                        index,
                        1
                    );

                    renderReferenceCards();
                }
            );

            footer.append(
                replace,
                remove
            );

            card.append(
                image,
                badges,
                footer
            );

            card.addEventListener(
                "dragstart",
                event => {
                    draggedReferenceIndex =
                        index;

                    card.classList.add(
                        "dragging"
                    );

                    event
                        .dataTransfer
                        .setData(
                            "text/plain",
                            String(index)
                        );
                }
            );

            card.addEventListener(
                "dragend",
                () => {
                    draggedReferenceIndex =
                        null;

                    card.classList.remove(
                        "dragging"
                    );

                    document
                        .querySelectorAll(
                            ".reference-card"
                        )
                        .forEach(
                            item =>
                                item.classList.remove(
                                    "drag-over"
                                )
                        );
                }
            );

            card.addEventListener(
                "dragover",
                event => {
                    event.preventDefault();

                    card.classList.add(
                        "drag-over"
                    );
                }
            );

            card.addEventListener(
                "dragleave",
                () => {
                    card.classList.remove(
                        "drag-over"
                    );
                }
            );

            card.addEventListener(
                "drop",
                event => {
                    event.preventDefault();

                    card.classList.remove(
                        "drag-over"
                    );

                    const source =
                        draggedReferenceIndex;

                    const target =
                        index;

                    if (
                        source === null
                        ||
                        source === target
                    ) {
                        return;
                    }

                    const [
                        moved
                    ] =
                        selectedImages.splice(
                            source,
                            1
                        );

                    selectedImages.splice(
                        target,
                        0,
                        moved
                    );

                    renderReferenceCards();
                }
            );

            imagePreviewGrid.appendChild(
                card
            );
        }
    );

    summaryImages.textContent =
        String(
            selectedImages.length
        );
}


/* =========================================================
   CREATIVE DIRECTION / OUTPUTS
========================================================= */

description.addEventListener(
    "input",
    () => {
        characterCount.textContent =
            `${description.value.length} characters`;
    }
);


document
    .querySelectorAll(
        ".count-button"
    )
    .forEach(
        button => {
            button.addEventListener(
                "click",
                () => {
                    document
                        .querySelectorAll(
                            ".count-button"
                        )
                        .forEach(
                            item =>
                                item.classList.remove(
                                    "selected"
                                )
                        );

                    button.classList.add(
                        "selected"
                    );

                    selectedCount =
                        button.dataset.count;

                    summaryCount.textContent =
                        selectedCount === "auto"
                            ?
                            "Auto"
                            :
                            selectedCount;

                    updateCreateCostEstimate();
                }
            );
        }
    );


/* =========================================================
   PIPELINE UI
========================================================= */

function resetPipeline() {
    [
        pipelineReferences,
        pipelinePlanner,
        pipelineVerify,
        pipelineImages,
    ].forEach(
        step => {
            step.classList.remove(
                "active",
                "complete",
                "error"
            );

            step.querySelector(
                "span"
            ).textContent =
                "Waiting";
        }
    );
}


function setPipelineStep(
    element,
    state,
    text
) {
    element.classList.remove(
        "active",
        "complete",
        "error"
    );

    if (state) {
        element.classList.add(
            state
        );
    }

    element.querySelector(
        "span"
    ).textContent =
        text;
}


function showPipeline(
    jobId
) {
    pipelineSection.classList.remove(
        "hidden-element"
    );

    pipelineJobId.textContent =
        `#${String(jobId).padStart(4, "0")}`;
}


/* =========================================================
   GENERATION JOB PIPELINE
========================================================= */

generateButton.addEventListener(
    "click",
    runCreateJob
);


async function runCreateJob() {
    if (!selectedProfileId) {
        showToast(
            "Choose a workflow first."
        );

        return;
    }

    if (!selectedImages.length) {
        showToast(
            "Add at least one product reference."
        );

        return;
    }

    stopImageBatchPolling();

    resultsSection.classList.add(
        "hidden-element"
    );

    imageBatchSection.classList.add(
        "hidden-element"
    );

    plannerResultSection.classList.add(
        "hidden-element"
    );

    promptPackagesSection.classList.add(
        "hidden-element"
    );

    currentPromptPackages =
        [];

    selectedCompareIds.clear();

    resetPipeline();

    setGenerateBusy(
        true,
        "UPLOADING REFERENCES"
    );

    const formData =
        new FormData();

    formData.append(
        "profile_id",
        String(
            selectedProfileId
        )
    );

    formData.append(
        "description",
        description.value.trim()
    );

    formData.append(
        "requested_count",
        selectedCount
    );

    selectedImages.forEach(
        file => {
            formData.append(
                "files",
                file,
                file.name
            );
        }
    );

    try {
        const response =
            await fetch(
                "/api/jobs",
                {
                    method: "POST",
                    body: formData,
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        currentJob =
            await response.json();

        renderPreparedJob(
            currentJob
        );

        showPipeline(
            currentJob.id
        );

        setPipelineStep(
            pipelineReferences,
            "complete",
            `${currentJob.reference_count} saved`
        );

        setPipelineStep(
            pipelinePlanner,
            "active",
            "Analyzing product"
        );

        setGenerateBusy(
            true,
            "PLANNING PROMPTS"
        );

        const planResponse =
            await fetch(
                `/api/jobs/${currentJob.id}/plan`,
                {
                    method: "POST"
                }
            );

        if (!planResponse.ok) {
            setPipelineStep(
                pipelinePlanner,
                "error",
                "Planner failed"
            );

            throw new Error(
                await apiError(
                    planResponse
                )
            );
        }

        currentJob =
            await planResponse.json();

        renderPlannerResult(
            currentJob
        );

        setPipelineStep(
            pipelinePlanner,
            "complete",
            `${currentJob.planner_provider || "AI"} plan ready`
        );

        setPipelineStep(
            pipelineVerify,
            "active",
            "Source checking"
        );

        setGenerateBusy(
            true,
            "VERIFYING PROMPTS"
        );

        const normalizeResponse =
            await fetch(
                `/api/jobs/${currentJob.id}/normalize`,
                {
                    method: "POST"
                }
            );

        if (!normalizeResponse.ok) {
            setPipelineStep(
                pipelineVerify,
                "error",
                "Verification failed"
            );

            throw new Error(
                await apiError(
                    normalizeResponse
                )
            );
        }

        const packageResponse =
            await fetch(
                `/api/jobs/${currentJob.id}/packages`
            );

        if (!packageResponse.ok) {
            throw new Error(
                await apiError(
                    packageResponse
                )
            );
        }

        const packages =
            await packageResponse.json();

        if (!packages.source_verified) {
            throw new Error(
                "Prompt source verification failed."
            );
        }

        renderPromptPackages(
            packages
        );

        setPipelineStep(
            pipelineVerify,
            "complete",
            `${packages.package_count} verified`
        );

        jobPanelStatus.textContent =
            "PROMPTS READY";

        if (
            autoGenerateImages.checked
        ) {
            setPipelineStep(
                pipelineImages,
                "active",
                "Starting"
            );

            await runImageBatch(
                currentJob.id
            );
        } else {
            setPipelineStep(
                pipelineImages,
                null,
                "Prompts only"
            );

            showToast(
                "Prompts are ready. Final image generation is off."
            );
        }

    } catch (error) {
        console.error(
            error
        );

        jobPanelStatus.textContent =
            "ERROR";

        showToast(
            error.message
        );

    } finally {
        setGenerateBusy(
            false,
            "GENERATE"
        );
    }
}


function setGenerateBusy(
    busy,
    label
) {
    generateButton.disabled =
        busy;

    generateButtonLabel.textContent =
        label;

    generateButtonArrow.textContent =
        busy
            ?
            "…"
            :
            "→";
}


function renderPreparedJob(
    job
) {
    jobEmptyState.classList.add(
        "hidden-element"
    );

    jobSavedState.classList.remove(
        "hidden-element"
    );

    currentJobId.textContent =
        `#${String(job.id).padStart(4, "0")}`;

    jobPanelStatus.textContent =
        "PREPARED";

    summaryProfile.textContent =
        job.profile_name
        ||
        summaryProfile.textContent;

    summaryImages.textContent =
        String(
            job.reference_count
            ||
            0
        );

    summaryCount.textContent =
        job.requested_count
        ===
        "auto"
            ?
            "Auto"
            :
            job.requested_count;

    storedReferenceGrid.innerHTML =
        "";

    (
        job.references
        ||
        []
    ).forEach(
        reference => {
            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "stored-reference";

            const image =
                document.createElement(
                    "img"
                );

            image.src =
                reference.file_url;

            image.alt =
                `Stored reference ${reference.position}`;

            const position =
                document.createElement(
                    "span"
                );

            position.textContent =
                reference.position;

            item.append(
                image,
                position
            );

            storedReferenceGrid.appendChild(
                item
            );
        }
    );
}


function renderPlannerResult(
    job
) {
    plannerResultSection.classList.remove(
        "hidden-element"
    );

    plannerResultModel.textContent =
        `${job.planner_provider || "AI"} · ${job.planner_model || "model"}`;

    plannerRawOutput.textContent =
        job.planner_raw_output
        ||
        "";

    summaryPlanner.textContent =
        `${capitalize(job.planner_provider || "AI")} · ${job.planner_model || "model"}`;
}


/* =========================================================
   PROMPT PACKAGES
========================================================= */

function renderPromptPackages(
    payload
) {
    currentPromptPackages =
        payload.packages
        ||
        [];

    promptPackagesCount.textContent =
        `${payload.package_count} READY`;

    promptPackageGrid.innerHTML =
        "";

    const negative =
        payload.shared_negative
        ||
        "";

    sharedNegativeText.textContent =
        negative;

    sharedNegativeBox.classList.toggle(
        "hidden-element",
        !negative
    );

    currentPromptPackages.forEach(
        item => {
            promptPackageGrid.appendChild(
                createPromptPackageCard(
                    item
                )
            );
        }
    );

    promptPackagesSection.classList.remove(
        "hidden-element"
    );
}


function createPromptPackageCard(
    item
) {
    const card =
        document.createElement(
            "article"
        );

    card.className =
        "prompt-package-card";

    const header =
        document.createElement(
            "header"
        );

    const number =
        document.createElement(
            "span"
        );

    number.textContent =
        `PROMPT ${item.position}`;

    const verified =
        document.createElement(
            "strong"
        );

    verified.textContent =
        "SOURCE VERIFIED";

    header.append(
        number,
        verified
    );

    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    const preview =
        document.createElement(
            "p"
        );

    preview.className =
        "prompt-package-preview";

    preview.textContent =
        item.positive_prompt_text;

    const tags =
        document.createElement(
            "div"
        );

    tags.className =
        "prompt-package-tags";

    const exact =
        document.createElement(
            "span"
        );

    exact.textContent =
        "POSITIVE · EXACT";

    tags.appendChild(
        exact
    );

    if (
        item.shared_negative_text
    ) {
        const negative =
            document.createElement(
                "span"
            );

        negative.textContent =
            "NEGATIVE · EXACT";

        tags.appendChild(
            negative
        );
    }

    const actions =
        document.createElement(
            "div"
        );

    actions.className =
        "prompt-package-actions";

    const copyOriginal =
        document.createElement(
            "button"
        );

    copyOriginal.type =
        "button";

    copyOriginal.textContent =
        "Copy original";

    copyOriginal.onclick =
        () =>
            copyText(
                item
                    .positive_prompt_text
            );

    const viewFinal =
        document.createElement(
            "button"
        );

    viewFinal.type =
        "button";

    viewFinal.className =
        "primary";

    viewFinal.textContent =
        "View final input";

    viewFinal.onclick =
        () =>
            openFinalInput(
                item
            );

    actions.append(
        copyOriginal,
        viewFinal
    );

    card.append(
        header,
        title,
        preview,
        tags,
        actions
    );

    return card;
}


function findPromptPackage(
    promptId
) {
    return (
        currentPromptPackages.find(
            item =>
                Number(
                    item.prompt_id
                )
                ===
                Number(
                    promptId
                )
        )
        ||
        null
    );
}


function openFinalInput(
    item
) {
    activeFinalPackage =
        item;

    finalInputTitle.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    finalInputStrategy.textContent =
        item.final_input_strategy
        ||
        "Source-verified prompt";

    finalInputPreview.textContent =
        item.final_input
        ||
        item.positive_prompt_text
        ||
        "";

    openModal(
        finalInputModal
    );
}


copyFinalInputModalButton
    .addEventListener(
        "click",
        () => {
            if (
                activeFinalPackage
            ) {
                copyText(
                    activeFinalPackage
                        .final_input
                    ||
                    ""
                );
            }
        }
    );


copyPlannerOutputButton
    .addEventListener(
        "click",
        () =>
            copyText(
                plannerRawOutput
                    .textContent
            )
    );


retryPlannerButton.addEventListener(
    "click",
    async () => {
        if (!currentJob) {
            return;
        }

        const confirmed =
            window.confirm(
                "Run the creative planner again for this job? Existing structured prompts will be replaced."
            );

        if (!confirmed) {
            return;
        }

        setPipelineStep(
            pipelinePlanner,
            "active",
            "Replanning"
        );

        retryPlannerButton.disabled =
            true;

        try {
            const response =
                await fetch(
                    `/api/jobs/${currentJob.id}/plan`,
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            currentJob =
                await response.json();

            renderPlannerResult(
                currentJob
            );

            const normalize =
                await fetch(
                    `/api/jobs/${currentJob.id}/normalize`,
                    {
                        method: "POST"
                    }
                );

            if (!normalize.ok) {
                throw new Error(
                    await apiError(
                        normalize
                    )
                );
            }

            const packages =
                await fetch(
                    `/api/jobs/${currentJob.id}/packages`
                );

            if (!packages.ok) {
                throw new Error(
                    await apiError(
                        packages
                    )
                );
            }

            renderPromptPackages(
                await packages.json()
            );

            setPipelineStep(
                pipelinePlanner,
                "complete",
                "Replanned"
            );

            setPipelineStep(
                pipelineVerify,
                "complete",
                "Verified"
            );

            showToast(
                "Planner output refreshed."
            );

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            retryPlannerButton.disabled =
                false;
        }
    }
);


/* =========================================================
   ADVANCED PANEL
========================================================= */

advancedPipelineToggle.addEventListener(
    "click",
    () => {
        advancedOpen =
            !advancedOpen;

        advancedContent.classList.toggle(
            "hidden-element",
            !advancedOpen
        );

        advancedToggleState.textContent =
            advancedOpen
                ?
                "Hide"
                :
                "Show";
    }
);


/* =========================================================
   IMAGE BATCH
========================================================= */

generateAllImagesButton.addEventListener(
    "click",
    async () => {
        if (!currentJob) {
            showToast(
                "Create a job first."
            );

            return;
        }

        await runImageBatch(
            currentJob.id
        );
    }
);


retryIncompleteImagesButton.addEventListener(
    "click",
    async () => {
        if (!currentJob) {
            return;
        }

        await runImageBatch(
            currentJob.id
        );
    }
);


refreshImageBatchButton.addEventListener(
    "click",
    async () => {
        if (!currentJob) {
            return;
        }

        await refreshImageBatch(
            currentJob.id
        );
    }
);


async function refreshImageBatch(
    jobId
) {
    try {
        const response =
            await fetch(
                `/api/jobs/${jobId}/image-batch`
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const payload =
            await response.json();

        renderImageBatch(
            payload
        );

        return payload;

    } catch (error) {
        console.error(
            error
        );

        return null;
    }
}


function renderImageBatch(
    payload
) {
    lastRenderedBatch =
        payload;

    imageBatchSection.classList.remove(
        "hidden-element"
    );

    const total =
        Number(
            payload.total_prompts
            ||
            0
        );

    const complete =
        Number(
            payload.complete_count
            ||
            0
        );

    const failed =
        Number(
            payload.failed_count
            ||
            0
        );

    const active =
        Number(
            payload.generating_count
            ||
            0
        )
        +
        Number(
            payload.queued_count
            ||
            0
        );

    const percent =
        total
            ?
            Math.round(
                (
                    complete
                    /
                    total
                )
                *
                100
            )
            :
            0;

    imageBatchCount.textContent =
        `${complete}/${total}`;

    imageBatchProgressBar.style.width =
        `${percent}%`;

    if (
        payload.status
        ===
        "complete"
    ) {
        imageBatchProgressText.textContent =
            "All images complete";
    } else if (active > 0) {
        imageBatchProgressText.textContent =
            `${active} generating · ${complete} complete`;
    } else if (failed > 0) {
        imageBatchProgressText.textContent =
            `${complete} complete · ${failed} failed`;
    } else {
        imageBatchProgressText.textContent =
            `${complete} complete · waiting`;
    }

    imageBatchFailureText.textContent =
        failed
            ?
            `${failed} FAILED`
            :
            "";

    imageBatchGrid.innerHTML =
        "";

    (
        payload.items
        ||
        []
    ).forEach(
        item => {
            imageBatchGrid.appendChild(
                createBatchCard(
                    item
                )
            );
        }
    );

    if (complete > 0) {
        renderResults(
            payload
        );
    }

    if (
        payload.status
        ===
        "complete"
    ) {
        setPipelineStep(
            pipelineImages,
            "complete",
            `${complete} ready`
        );

        jobPanelStatus.textContent =
            "IMAGES READY";
    }

    if (
        payload.status
        ===
        "partial_failed"
        ||
        payload.status
        ===
        "failed"
    ) {
        setPipelineStep(
            pipelineImages,
            "error",
            `${failed} failed`
        );
    }

    retryIncompleteImagesButton.disabled =
        imageBatchRequestRunning
        ||
        (
            total > 0
            &&
            complete === total
        );
}


function createBatchCard(
    item
) {
    const card =
        document.createElement(
            "article"
        );

    card.className =
        `image-batch-card status-${item.status}`;

    const header =
        document.createElement(
            "header"
        );

    const number =
        document.createElement(
            "span"
        );

    number.textContent =
        `PROMPT ${item.position}`;

    const status =
        document.createElement(
            "strong"
        );

    status.textContent =
        String(
            item.status
            ||
            "pending"
        ).toUpperCase();

    header.append(
        number,
        status
    );

    const media =
        document.createElement(
            "div"
        );

    media.className =
        "image-batch-media";

    if (
        item.status
        ===
        "complete"
        &&
        item.image?.file_url
    ) {
        const image =
            document.createElement(
                "img"
            );

        image.src =
            item.image.file_url;

        image.alt =
            item.title
            ||
            `Generated image ${item.position}`;

        media.appendChild(
            image
        );
    } else {
        const placeholder =
            document.createElement(
                "div"
            );

        placeholder.className =
            "image-batch-placeholder";

        placeholder.textContent =
            {
                generating:
                    "GENERATING…",
                queued:
                    "QUEUED",
                failed:
                    "FAILED",
                pending:
                    "WAITING",
            }[
                item.status
            ]
            ||
            "WAITING";

        media.appendChild(
            placeholder
        );
    }

    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    card.append(
        header,
        media,
        title
    );

    if (
        item.status
        ===
        "failed"
        &&
        item.image
            ?.error_message
    ) {
        const error =
            document.createElement(
                "p"
            );

        error.className =
            "image-batch-error";

        error.textContent =
            friendlyError(
                item.image
                    .error_message
            );

        card.appendChild(
            error
        );
    }

    return card;
}


async function runImageBatch(
    jobId
) {
    if (
        imageBatchRequestRunning
    ) {
        showToast(
            "Image generation is already running."
        );

        return false;
    }

    imageBatchRequestRunning =
        true;

    imageBatchSection.classList.remove(
        "hidden-element"
    );

    generateAllImagesButton.disabled =
        true;

    retryIncompleteImagesButton.disabled =
        true;

    setPipelineStep(
        pipelineImages,
        "active",
        "Generating"
    );

    setGenerateBusy(
        true,
        "GENERATING IMAGES"
    );

    jobPanelStatus.textContent =
        "GENERATING";

    await refreshImageBatch(
        jobId
    );

    startImageBatchPolling(
        jobId
    );

    try {
        const response =
            await fetch(
                `/api/jobs/${jobId}/generate-all-images`,
                {
                    method: "POST"
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        await response.json();

        const finalStatus =
            await refreshImageBatch(
                jobId
            );

        if (!finalStatus) {
            throw new Error(
                "Could not read final image status."
            );
        }

        if (
            finalStatus.status
            ===
            "complete"
        ) {
            showToast(
                `All ${finalStatus.complete_count} images are ready.`
            );

            resultsSection.scrollIntoView({
                behavior:
                    "smooth",
                block:
                    "start",
            });

            return true;
        }

        if (
            finalStatus.status
            ===
            "partial_failed"
        ) {
            showToast(
                `${finalStatus.complete_count} completed; ${finalStatus.failed_count} failed. Retry skips completed images.`
            );

            return true;
        }

        throw new Error(
            "Image generation did not complete."
        );

    } catch (error) {
        setPipelineStep(
            pipelineImages,
            "error",
            "Generation failed"
        );

        jobPanelStatus.textContent =
            "IMAGE ERROR";

        showToast(
            error.message
        );

        return false;

    } finally {
        imageBatchRequestRunning =
            false;

        generateAllImagesButton.disabled =
            false;

        setGenerateBusy(
            false,
            "GENERATE"
        );

        stopImageBatchPolling();
    }
}


function startImageBatchPolling(
    jobId
) {
    stopImageBatchPolling();

    imageBatchPollTimer =
        setInterval(
            async () => {
                const payload =
                    await refreshImageBatch(
                        jobId
                    );

                if (
                    !imageBatchRequestRunning
                    &&
                    payload
                    &&
                    [
                        "complete",
                        "partial_failed",
                        "failed",
                    ].includes(
                        payload.status
                    )
                ) {
                    stopImageBatchPolling();
                }
            },
            1500
        );
}


function stopImageBatchPolling() {
    if (
        imageBatchPollTimer
    ) {
        clearInterval(
            imageBatchPollTimer
        );

        imageBatchPollTimer =
            null;
    }
}


/* =========================================================
   RESULTS GALLERY
========================================================= */

function renderResults(
    batch
) {
    const completeItems =
        (
            batch.items
            ||
            []
        )
        .filter(
            item =>
                item.status
                ===
                "complete"
                &&
                item.image
                    ?.file_url
        );

    if (!completeItems.length) {
        resultsSection.classList.add(
            "hidden-element"
        );

        return;
    }

    resultsSection.classList.remove(
        "hidden-element"
    );

    resultsSubtitle.textContent =
        `${completeItems.length} of ${batch.total_prompts} outputs complete.`;

    downloadAllButton.href =
        `/api/jobs/${batch.job_id}/download.zip`;

    resultsGrid.innerHTML =
        "";

    selectedCompareIds =
        new Set(
            [
                ...selectedCompareIds
            ].filter(
                id =>
                    completeItems.some(
                        item =>
                            Number(
                                item.image.id
                            )
                            ===
                            Number(id)
                    )
            )
        );

    completeItems.forEach(
        item => {
            resultsGrid.appendChild(
                createResultCard(
                    item
                )
            );
        }
    );

    previewResults =
        completeItems;

    previewPackageLookup =
        currentPromptPackages;

    previewJobId =
        currentJob?.id
        ??
        batch.job_id
        ??
        null;

    updateCompareButton();
}


function createResultCard(
    item
) {
    const card =
        document.createElement(
            "article"
        );

    card.className =
        "result-card";

    const media =
        document.createElement(
            "div"
        );

    media.className =
        "result-card-media";

    const image =
        document.createElement(
            "img"
        );

    image.src =
        item.image.file_url;

    image.alt =
        item.title
        ||
        `Generated image ${item.position}`;

    image.loading =
        "lazy";

    image.addEventListener(
        "click",
        () => {
            openImagePreviewById(
                item.image.id
            );
        }
    );

    const selectLabel =
        document.createElement(
            "label"
        );

    selectLabel.className =
        "result-card-select";

    const checkbox =
        document.createElement(
            "input"
        );

    checkbox.type =
        "checkbox";

    checkbox.checked =
        selectedCompareIds.has(
            Number(
                item.image.id
            )
        );

    checkbox.addEventListener(
        "change",
        () => {
            const id =
                Number(
                    item.image.id
                );

            if (
                checkbox.checked
            ) {
                selectedCompareIds.add(
                    id
                );

                if (
                    selectedCompareIds.size
                    >
                    2
                ) {
                    const first =
                        [
                            ...selectedCompareIds
                        ][0];

                    selectedCompareIds.delete(
                        first
                    );

                    if (
                        lastRenderedBatch
                    ) {
                        renderResults(
                            lastRenderedBatch
                        );
                    }
                }
            } else {
                selectedCompareIds.delete(
                    id
                );
            }

            updateCompareButton();
        }
    );

    const compareText =
        document.createElement(
            "span"
        );

    compareText.textContent =
        "COMPARE";

    selectLabel.append(
        checkbox,
        compareText
    );

    const provider =
        document.createElement(
            "span"
        );

    provider.className =
        "result-card-provider";

    provider.textContent =
        providerLabel(
            item.image.provider
        );

    const favorite =
        document.createElement(
            "button"
        );

    favorite.type =
        "button";

    favorite.className =
        "result-card-favorite";

    favorite.classList.toggle(
        "active",
        Boolean(
            item.image.is_favorite
        )
    );

    favorite.textContent =
        item.image.is_favorite
            ?
            "★"
            :
            "☆";

    favorite.title =
        "Mark this output as a favorite";

    favorite.addEventListener(
        "click",
        async event => {
            event.stopPropagation();

            const nextValue =
                !Boolean(
                    item.image.is_favorite
                );

            const updated =
                await toggleImageFavorite(
                    item.image.id,
                    nextValue
                );

            if (updated) {
                item.image.is_favorite =
                    nextValue;

                favorite.classList.toggle(
                    "active",
                    nextValue
                );

                favorite.textContent =
                    nextValue
                        ?
                        "★"
                        :
                        "☆";
            }
        }
    );

    media.append(
        image,
        selectLabel,
        provider,
        favorite
    );

    const body =
        document.createElement(
            "div"
        );

    body.className =
        "result-card-body";

    const label =
        document.createElement(
            "span"
        );

    label.className =
        "result-card-label";

    label.textContent =
        `IMAGE ${item.position}`;

    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    const meta =
        document.createElement(
            "div"
        );

    meta.className =
        "result-card-meta";

    meta.textContent =
        providerMeta(
            item.image.provider
        );

    const actions =
        document.createElement(
            "div"
        );

    actions.className =
        "result-actions";

    const view =
        document.createElement(
            "button"
        );

    view.type =
        "button";

    view.className =
        "result-primary";

    view.textContent =
        "View";

    view.onclick =
        () =>
            openImagePreviewById(
                item.image.id
            );

    const regenerate =
        document.createElement(
            "button"
        );

    regenerate.type =
        "button";

    regenerate.textContent =
        "Regenerate";

    regenerate.onclick =
        () =>
            openRegenerate(
                item
            );

    const download =
        document.createElement(
            "a"
        );

    download.href =
        `/api/images/${item.image.id}/download`;

    download.textContent =
        "Download";

    actions.append(
        view,
        regenerate,
        download
    );

    body.append(
        label,
        title,
        meta,
        actions
    );

    card.append(
        media,
        body
    );

    return card;
}


function updateCompareButton() {
    compareSelectedButton.disabled =
        selectedCompareIds.size
        !==
        2;

    compareSelectedButton.textContent =
        selectedCompareIds.size
        ===
        2
            ?
            "Compare selected"
            :
            "Compare 2";
}


compareSelectedButton.addEventListener(
    "click",
    () => {
        if (
            selectedCompareIds.size
            !==
            2
        ) {
            return;
        }

        const ids =
            [
                ...selectedCompareIds
            ];

        const items =
            previewResults.filter(
                item =>
                    ids.includes(
                        Number(
                            item.image.id
                        )
                    )
            );

        if (
            items.length
            !==
            2
        ) {
            return;
        }

        compareImageA.src =
            items[0]
                .image
                .file_url;

        compareTitleA.textContent =
            items[0].title;

        compareImageB.src =
            items[1]
                .image
                .file_url;

        compareTitleB.textContent =
            items[1].title;

        openModal(
            compareModal
        );
    }
);


/* =========================================================
   IMAGE PREVIEW
========================================================= */

function openImagePreviewById(
    imageId
) {
    const index =
        previewResults.findIndex(
            item =>
                Number(
                    item.image.id
                )
                ===
                Number(
                    imageId
                )
        );

    if (index < 0) {
        return;
    }

    previewIndex =
        index;

    renderPreview();

    openModal(
        imagePreviewModal
    );
}


function renderPreview() {
    const item =
        previewResults[
            previewIndex
        ];

    if (!item) {
        return;
    }

    previewImagePosition.textContent =
        `IMAGE ${previewIndex + 1} / ${previewResults.length}`;

    previewImageTitle.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    previewLargeImage.src =
        item.image.file_url;

    previewProviderMeta.textContent =
        providerMeta(
            item.image.provider
        );

    previewDownloadButton.href =
        `/api/images/${item.image.id}/download`;

    previewPreviousButton.disabled =
        previewResults.length < 2;

    previewNextButton.disabled =
        previewResults.length < 2;
}


previewPreviousButton.addEventListener(
    "click",
    () => {
        if (!previewResults.length) {
            return;
        }

        previewIndex =
            (
                previewIndex
                -
                1
                +
                previewResults.length
            )
            %
            previewResults.length;

        renderPreview();
    }
);


previewNextButton.addEventListener(
    "click",
    () => {
        if (!previewResults.length) {
            return;
        }

        previewIndex =
            (
                previewIndex
                +
                1
            )
            %
            previewResults.length;

        renderPreview();
    }
);


previewPromptButton.addEventListener(
    "click",
    () => {
        const item =
            previewResults[
                previewIndex
            ];

        if (!item) {
            return;
        }

        const packageItem =
            (
                previewPackageLookup
                ||
                []
            ).find(
                packageItem =>
                    Number(
                        packageItem.prompt_id
                    )
                    ===
                    Number(
                        item.prompt_id
                    )
            )
            ||
            findPromptPackage(
                item.prompt_id
            );

        if (packageItem) {
            openFinalInput(
                packageItem
            );
        }
    }
);


previewRegenerateButton.addEventListener(
    "click",
    () => {
        const item =
            previewResults[
                previewIndex
            ];

        if (item) {
            closeModal(
                imagePreviewModal
            );

            openRegenerate(
                item,
                previewJobId
                ??
                currentJob?.id
            );
        }
    }
);


/* =========================================================
   REGENERATE ONE
========================================================= */

function openRegenerate(
    item,
    jobId = currentJob?.id
) {
    regenerateTarget =
        item;

    regenerateJobId =
        jobId
        ??
        null;

    regenerateDirection.value =
        "";

    regenerateTitle.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    openModal(
        regenerateModal
    );
}


confirmRegenerateButton.addEventListener(
    "click",
    async () => {
        if (
            !regenerateJobId
            ||
            !regenerateTarget
        ) {
            return;
        }

        confirmRegenerateButton.disabled =
            true;

        confirmRegenerateButton.textContent =
            "Generating…";

        try {
            const response =
                await fetch(
                    `/api/jobs/${regenerateJobId}/prompts/${regenerateTarget.prompt_id}/regenerate-image`,
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                extra_direction:
                                    regenerateDirection
                                        .value
                                        .trim()
                            }),
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            await response.json();

            closeModal(
                regenerateModal
            );

            if (
                currentJob
                &&
                Number(
                    currentJob.id
                )
                ===
                Number(
                    regenerateJobId
                )
            ) {
                const batch =
                    await refreshImageBatch(
                        currentJob.id
                    );

                if (batch) {
                    renderResults(
                        batch
                    );
                }
            }

            if (
                historyDetail
                &&
                Number(
                    historyDetail.id
                )
                ===
                Number(
                    regenerateJobId
                )
            ) {
                await openHistoryJob(
                    historyDetail.id,
                    {
                        preserveModal:
                            true
                    }
                );
            }

            showToast(
                "Regenerated image is ready."
            );

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            confirmRegenerateButton.disabled =
                false;

            confirmRegenerateButton.textContent =
                "Regenerate";
        }
    }
);


/* =========================================================
   STEP 12 — HISTORY / CREATIVE LIBRARY
========================================================= */

async function ensureHistoryOptions() {
    if (historyOptions) {
        return historyOptions;
    }

    try {
        const response =
            await fetch(
                "/api/history/options"
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        historyOptions =
            await response.json();

        populateHistoryFilters();

        return historyOptions;

    } catch (error) {
        showToast(
            error.message
        );

        return null;
    }
}


function populateHistoryFilters() {
    if (!historyOptions) {
        return;
    }

    const currentProfile =
        historyProfileFilter.value;

    historyProfileFilter.innerHTML = `
        <option value="">
            All workflows
        </option>
    `;

    historyOptions.profiles.forEach(
        profile => {
            const option =
                document.createElement(
                    "option"
                );

            option.value =
                String(
                    profile.id
                );

            option.textContent =
                profile.name;

            historyProfileFilter.appendChild(
                option
            );
        }
    );

    if (
        [
            ...historyProfileFilter.options
        ].some(
            option =>
                option.value
                ===
                currentProfile
        )
    ) {
        historyProfileFilter.value =
            currentProfile;
    }

    historyStatusFilter.innerHTML = `
        <option value="">
            All statuses
        </option>
    `;

    const statusLabels = {
        complete:
            "Complete",
        partial:
            "Partial",
        prompts_ready:
            "Prompts ready",
        planned:
            "Planned",
        failed:
            "Failed",
        prepared:
            "Prepared",
    };

    historyOptions.statuses.forEach(
        value => {
            const option =
                document.createElement(
                    "option"
                );

            option.value =
                value;

            option.textContent =
                statusLabels[value]
                ||
                capitalize(
                    value.replaceAll(
                        "_",
                        " "
                    )
                );

            historyStatusFilter.appendChild(
                option
            );
        }
    );

    fillHistoryProviderSelect(
        historyPlannerFilter,
        historyOptions
            .planner_providers,
        "Any planner"
    );

    fillHistoryProviderSelect(
        historyImageProviderFilter,
        historyOptions
            .image_providers,
        "Any image provider"
    );
}


function fillHistoryProviderSelect(
    element,
    values,
    emptyLabel
) {
    const current =
        element.value;

    element.innerHTML =
        "";

    const empty =
        document.createElement(
            "option"
        );

    empty.value =
        "";

    empty.textContent =
        emptyLabel;

    element.appendChild(
        empty
    );

    values.forEach(
        value => {
            const option =
                document.createElement(
                    "option"
                );

            option.value =
                value;

            option.textContent =
                value === "openai"
                    ?
                    "OpenAI"
                    :
                    "Gemini";

            element.appendChild(
                option
            );
        }
    );

    if (
        [
            ...element.options
        ].some(
            option =>
                option.value
                ===
                current
        )
    ) {
        element.value =
            current;
    }
}


function historyQueryParams() {
    const params =
        new URLSearchParams();

    const query =
        historySearchInput
            .value
            .trim();

    if (query) {
        params.set(
            "q",
            query
        );
    }

    if (
        historyProfileFilter.value
    ) {
        params.set(
            "profile_id",
            historyProfileFilter.value
        );
    }

    if (
        historyStatusFilter.value
    ) {
        params.set(
            "status",
            historyStatusFilter.value
        );
    }

    if (
        historyPlannerFilter.value
    ) {
        params.set(
            "planner_provider",
            historyPlannerFilter.value
        );
    }

    if (
        historyImageProviderFilter.value
    ) {
        params.set(
            "image_provider",
            historyImageProviderFilter.value
        );
    }

    if (
        historyFavoritesOnly.checked
    ) {
        params.set(
            "favorites_only",
            "true"
        );
    }

    params.set(
        "limit",
        "150"
    );

    return params;
}


async function loadHistory() {
    historyGrid.innerHTML = `
        <div class="history-loading-state">
            Loading creative history…
        </div>
    `;

    historyEmptyState.classList.add(
        "hidden-element"
    );

    try {
        const params =
            historyQueryParams();

        const response =
            await fetch(
                `/api/history?${params.toString()}`
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const payload =
            await response.json();

        historyItems =
            payload.items
            ||
            [];

        historyCountLabel.textContent =
            String(
                payload.total
                ??
                historyItems.length
            );

        renderHistoryCards();

    } catch (error) {
        historyGrid.innerHTML = `
            <div class="history-loading-state">
                Could not load history.
            </div>
        `;

        showToast(
            error.message
        );
    }
}


function renderHistoryCards() {
    historyGrid.innerHTML =
        "";

    if (!historyItems.length) {
        historyEmptyState.classList.remove(
            "hidden-element"
        );

        return;
    }

    historyEmptyState.classList.add(
        "hidden-element"
    );

    historyItems.forEach(
        item => {
            historyGrid.appendChild(
                createHistoryCard(
                    item
                )
            );
        }
    );
}


function createHistoryCard(
    item
) {
    const card =
        document.createElement(
            "article"
        );

    card.className =
        "history-card";

    const thumbs =
        document.createElement(
            "div"
        );

    thumbs.className =
        "history-card-thumbnails";

    const thumbnails =
        item.thumbnails
        ||
        [];

    if (
        thumbnails.length
        ===
        1
    ) {
        thumbs.classList.add(
            "single"
        );
    }

    if (
        thumbnails.length
        ===
        2
    ) {
        thumbs.classList.add(
            "two"
        );
    }

    if (thumbnails.length) {
        thumbnails.forEach(
            thumb => {
                const image =
                    document.createElement(
                        "img"
                    );

                image.src =
                    thumb.url;

                image.alt =
                    `${item.profile_name} history thumbnail`;

                image.loading =
                    "lazy";

                thumbs.appendChild(
                    image
                );
            }
        );
    } else {
        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "history-card-empty-thumb";

        empty.textContent =
            "NO PREVIEW";

        thumbs.appendChild(
            empty
        );
    }

    const type =
        document.createElement(
            "span"
        );

    type.className =
        "history-card-type-badge";

    type.textContent =
        thumbnails.some(
            thumb =>
                thumb.type
                ===
                "generated"
        )
            ?
            "GENERATED"
            :
            "REFERENCE";

    const status =
        document.createElement(
            "span"
        );

    status.className =
        (
            "history-card-status "
            +
            item.display_status
        );

    status.textContent =
        historyStatusLabel(
            item.display_status
        );

    thumbs.append(
        type,
        status
    );

    const body =
        document.createElement(
            "div"
        );

    body.className =
        "history-card-body";

    const heading =
        document.createElement(
            "div"
        );

    heading.className =
        "history-card-heading";

    const left =
        document.createElement(
            "div"
        );

    const kicker =
        document.createElement(
            "span"
        );

    kicker.textContent =
        (
            `JOB #${String(item.id).padStart(4, "0")}`
            +
            (
                item.has_favorite_output
                    ?
                    " · ★ WINNER"
                    :
                    ""
            )
        );

    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        item.profile_name;

    left.append(
        kicker,
        title
    );

    const favorite =
        document.createElement(
            "button"
        );

    favorite.type =
        "button";

    favorite.className =
        "history-job-star";

    favorite.classList.toggle(
        "active",
        Boolean(
            item.is_favorite
        )
    );

    favorite.textContent =
        item.is_favorite
            ?
            "★"
            :
            "☆";

    favorite.title =
        "Favorite this job";

    favorite.addEventListener(
        "click",
        async event => {
            event.stopPropagation();

            const next =
                !Boolean(
                    item.is_favorite
                );

            const updated =
                await toggleJobFavorite(
                    item.id,
                    next
                );

            if (updated) {
                item.is_favorite =
                    next;

                favorite.classList.toggle(
                    "active",
                    next
                );

                favorite.textContent =
                    next
                        ?
                        "★"
                        :
                        "☆";

                if (
                    historyFavoritesOnly.checked
                    &&
                    !next
                    &&
                    !item.has_favorite_output
                ) {
                    await loadHistory();
                }
            }
        }
    );

    heading.append(
        left,
        favorite
    );

    const desc =
        document.createElement(
            "p"
        );

    desc.className =
        "history-card-description";

    desc.textContent =
        item.description
        ||
        "No additional creative direction.";

    const meta =
        document.createElement(
            "div"
        );

    meta.className =
        "history-card-meta";

    meta.append(
        historyMetaCell(
            "DATE",
            formatHistoryDate(
                item.created_at
            )
        ),

        historyMetaCell(
            "OUTPUTS",
            `${item.complete_count || 0}/${item.prompt_count || 0}`
        ),

        historyMetaCell(
            "PLANNER",
            (
                item.planner_provider
                    ?
                    `${capitalize(item.planner_provider)} · ${item.planner_model || "model"}`
                    :
                    "—"
            )
        ),

        historyMetaCell(
            "IMAGE ENGINE",
            (
                item.image_provider
                    ?
                    `${capitalize(item.image_provider)} · ${item.image_model || "model"}`
                    :
                    "Not generated"
            )
        )
    );

    const actions =
        document.createElement(
            "div"
        );

    actions.className =
        "history-card-actions";

    const open =
        document.createElement(
            "button"
        );

    open.type =
        "button";

    open.className =
        "history-primary";

    open.textContent =
        "Open job";

    open.onclick =
        () =>
            openHistoryJob(
                item.id
            );

    const duplicate =
        document.createElement(
            "button"
        );

    duplicate.type =
        "button";

    duplicate.textContent =
        "Duplicate";

    duplicate.onclick =
        async () => {
            const detail =
                await fetchHistoryDetail(
                    item.id
                );

            if (detail) {
                await duplicateHistoryJob(
                    detail
                );
            }
        };

    actions.append(
        open,
        duplicate
    );

    body.append(
        heading,
        desc,
        meta,
        actions
    );

    card.append(
        thumbs,
        body
    );

    return card;
}


function historyMetaCell(
    label,
    value
) {
    const cell =
        document.createElement(
            "div"
        );

    const key =
        document.createElement(
            "span"
        );

    key.textContent =
        label;

    const data =
        document.createElement(
            "strong"
        );

    data.textContent =
        value;

    cell.append(
        key,
        data
    );

    return cell;
}


function historyStatusLabel(
    value
) {
    const labels = {
        complete:
            "COMPLETE",
        partial:
            "PARTIAL",
        prompts_ready:
            "PROMPTS READY",
        planned:
            "PLANNED",
        failed:
            "FAILED",
        prepared:
            "PREPARED",
        planning:
            "PLANNING",
        normalizing:
            "VERIFYING",
    };

    return labels[value]
        ||
        String(
            value
            ||
            "JOB"
        )
        .replaceAll(
            "_",
            " "
        )
        .toUpperCase();
}


function formatHistoryDate(
    value
) {
    if (!value) {
        return "—";
    }

    const normalized =
        value.includes(
            "T"
        )
            ?
            value
            :
            value.replace(
                " ",
                "T"
            )
            +
            "Z";

    const date =
        new Date(
            normalized
        );

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {
        return value;
    }

    return date.toLocaleString(
        [],
        {
            month:
                "short",
            day:
                "numeric",
            hour:
                "numeric",
            minute:
                "2-digit",
        }
    );
}


async function fetchHistoryDetail(
    jobId
) {
    try {
        const response =
            await fetch(
                `/api/history/${jobId}`
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        return await response.json();

    } catch (error) {
        showToast(
            error.message
        );

        return null;
    }
}


async function openHistoryJob(
    jobId,
    options = {}
) {
    const detail =
        await fetchHistoryDetail(
            jobId
        );

    if (!detail) {
        return;
    }

    historyDetail =
        detail;

    renderHistoryDetail(
        detail
    );

    if (
        !options.preserveModal
    ) {
        openModal(
            historyDetailModal
        );
    }
}


function renderHistoryDetail(
    detail
) {
    historyDetailKicker.textContent =
        `JOB #${String(detail.id).padStart(4, "0")}`;

    historyDetailTitle.textContent =
        detail.profile_name
        ||
        "Image job";

    historyDetailMeta.textContent =
        (
            `${formatHistoryDate(detail.created_at)}`
            +
            ` · ${historyStatusLabel(detail.batch?.status || detail.status)}`
        );

    historyDetailFavoriteButton.classList.toggle(
        "active",
        Boolean(
            detail.is_favorite
        )
    );

    historyDetailFavoriteButton.textContent =
        detail.is_favorite
            ?
            "★"
            :
            "☆";

    historyDownloadAllButton.href =
        `/api/jobs/${detail.id}/download.zip`;

    historyDetailWorkflow.textContent =
        detail.profile_name
        ||
        "—";

    historyDetailPlanner.textContent =
        detail.planner_provider
            ?
            `${capitalize(detail.planner_provider)} · ${detail.planner_model || "model"}`
            :
            "—";

    const completeItems =
        (
            detail.batch?.items
            ||
            []
        )
        .filter(
            item =>
                item.status
                ===
                "complete"
                &&
                item.image
                    ?.file_url
        );

    const firstImage =
        completeItems[0]
            ?.image;

    historyDetailImageEngine.textContent =
        firstImage
            ?
            providerMeta(
                firstImage.provider
            )
            :
            "Not generated";

    historyDetailOutputs.textContent =
        `${detail.batch?.complete_count || 0}/${detail.batch?.total_prompts || 0}`;

    historyDetailDirection.textContent =
        detail.description
        ||
        "No additional creative direction.";

    renderHistoryReferences(
        detail.references
        ||
        []
    );

    renderHistoryOutputs(
        detail,
        completeItems
    );

    renderHistoryPrompts(
        detail.packages
            ?.packages
        ||
        []
    );
}


function renderHistoryReferences(
    references
) {
    historyDetailReferenceCount.textContent =
        String(
            references.length
        );

    historyDetailReferences.innerHTML =
        "";

    references.forEach(
        reference => {
            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "history-reference-card";

            const image =
                document.createElement(
                    "img"
                );

            image.src =
                reference.file_url;

            image.alt =
                `Reference ${reference.position}`;

            const label =
                document.createElement(
                    "span"
                );

            label.textContent =
                reference.position === 1
                    ?
                    "1 · PRIMARY"
                    :
                    String(
                        reference.position
                    );

            card.append(
                image,
                label
            );

            historyDetailReferences.appendChild(
                card
            );
        }
    );
}


function renderHistoryOutputs(
    detail,
    completeItems
) {
    historyDetailImageCount.textContent =
        String(
            completeItems.length
        );

    historyDetailImages.innerHTML =
        "";

    if (!completeItems.length) {
        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "history-loading-state";

        empty.textContent =
            "No completed images for this job.";

        historyDetailImages.appendChild(
            empty
        );

        return;
    }

    completeItems.forEach(
        item => {
            historyDetailImages.appendChild(
                createHistoryOutputCard(
                    detail,
                    item,
                    completeItems
                )
            );
        }
    );
}


function createHistoryOutputCard(
    detail,
    item,
    completeItems
) {
    const card =
        document.createElement(
            "article"
        );

    card.className =
        "history-output-card";

    const media =
        document.createElement(
            "div"
        );

    media.className =
        "history-output-media";

    const image =
        document.createElement(
            "img"
        );

    image.src =
        item.image.file_url;

    image.alt =
        item.title
        ||
        `Generated output ${item.position}`;

    image.onclick =
        () => {
            previewResults =
                completeItems;

            previewPackageLookup =
                detail.packages
                    ?.packages
                ||
                [];

            previewJobId =
                detail.id;

            openImagePreviewById(
                item.image.id
            );
        };

    const favorite =
        document.createElement(
            "button"
        );

    favorite.type =
        "button";

    favorite.className =
        "history-output-star";

    favorite.classList.toggle(
        "active",
        Boolean(
            item.image.is_favorite
        )
    );

    favorite.textContent =
        item.image.is_favorite
            ?
            "★"
            :
            "☆";

    favorite.title =
        "Mark as favorite output";

    favorite.onclick =
        async event => {
            event.stopPropagation();

            const next =
                !Boolean(
                    item.image.is_favorite
                );

            const updated =
                await toggleImageFavorite(
                    item.image.id,
                    next
                );

            if (updated) {
                item.image.is_favorite =
                    next;

                favorite.classList.toggle(
                    "active",
                    next
                );

                favorite.textContent =
                    next
                        ?
                        "★"
                        :
                        "☆";

                await loadHistory();
            }
        };

    media.append(
        image,
        favorite
    );

    const body =
        document.createElement(
            "div"
        );

    body.className =
        "history-output-body";

    const label =
        document.createElement(
            "span"
        );

    label.textContent =
        `IMAGE ${item.position}`;

    const title =
        document.createElement(
            "h3"
        );

    title.textContent =
        item.title
        ||
        `Prompt ${item.position}`;

    const actions =
        document.createElement(
            "div"
        );

    actions.className =
        "history-output-actions";

    const view =
        document.createElement(
            "button"
        );

    view.type =
        "button";

    view.textContent =
        "View";

    view.onclick =
        () => {
            previewResults =
                completeItems;

            previewPackageLookup =
                detail.packages
                    ?.packages
                ||
                [];

            previewJobId =
                detail.id;

            openImagePreviewById(
                item.image.id
            );
        };

    const prompt =
        document.createElement(
            "button"
        );

    prompt.type =
        "button";

    prompt.textContent =
        "Prompt";

    prompt.onclick =
        () => {
            const packageItem =
                (
                    detail.packages
                        ?.packages
                    ||
                    []
                ).find(
                    candidate =>
                        Number(
                            candidate.prompt_id
                        )
                        ===
                        Number(
                            item.prompt_id
                        )
                );

            if (packageItem) {
                openFinalInput(
                    packageItem
                );
            }
        };

    const download =
        document.createElement(
            "a"
        );

    download.href =
        `/api/images/${item.image.id}/download`;

    download.textContent =
        "Download";

    actions.append(
        view,
        prompt,
        download
    );

    body.append(
        label,
        title,
        actions
    );

    card.append(
        media,
        body
    );

    return card;
}


function renderHistoryPrompts(
    packages
) {
    historyDetailPrompts.innerHTML =
        "";

    if (!packages.length) {
        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "history-prompt-item";

        empty.textContent =
            "No source-verified prompt packages saved.";

        historyDetailPrompts.appendChild(
            empty
        );

        return;
    }

    packages.forEach(
        item => {
            const block =
                document.createElement(
                    "article"
                );

            block.className =
                "history-prompt-item";

            const title =
                document.createElement(
                    "strong"
                );

            title.textContent =
                item.title
                ||
                `Prompt ${item.position}`;

            const copy =
                document.createElement(
                    "p"
                );

            copy.textContent =
                item.positive_prompt_text
                ||
                item.final_input
                ||
                "";

            const view =
                document.createElement(
                    "button"
                );

            view.type =
                "button";

            view.textContent =
                "View exact input";

            view.onclick =
                () =>
                    openFinalInput(
                        item
                    );

            block.append(
                title,
                copy,
                view
            );

            historyDetailPrompts.appendChild(
                block
            );
        }
    );
}


async function toggleJobFavorite(
    jobId,
    favorite
) {
    try {
        const response =
            await fetch(
                `/api/history/${jobId}/favorite`,
                {
                    method:
                        "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            favorite:
                                Boolean(
                                    favorite
                                )
                        }),
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        return await response.json();

    } catch (error) {
        showToast(
            error.message
        );

        return null;
    }
}


async function toggleImageFavorite(
    imageId,
    favorite
) {
    try {
        const response =
            await fetch(
                `/api/images/${imageId}/favorite`,
                {
                    method:
                        "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            favorite:
                                Boolean(
                                    favorite
                                )
                        }),
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        return await response.json();

    } catch (error) {
        showToast(
            error.message
        );

        return null;
    }
}


historyDetailFavoriteButton.addEventListener(
    "click",
    async () => {
        if (!historyDetail) {
            return;
        }

        const next =
            !Boolean(
                historyDetail.is_favorite
            );

        const updated =
            await toggleJobFavorite(
                historyDetail.id,
                next
            );

        if (!updated) {
            return;
        }

        historyDetail.is_favorite =
            next;

        historyDetailFavoriteButton.classList.toggle(
            "active",
            next
        );

        historyDetailFavoriteButton.textContent =
            next
                ?
                "★"
                :
                "☆";

        await loadHistory();
    }
);


historyDuplicateButton.addEventListener(
    "click",
    async () => {
        if (
            historyDetail
        ) {
            await duplicateHistoryJob(
                historyDetail
            );
        }
    }
);


async function duplicateHistoryJob(
    detail
) {
    historyDuplicateButton.disabled =
        true;

    historyDuplicateButton.textContent =
        "Loading references…";

    try {
        await loadProfiles(
            detail.profile_id
        );

        const profileExists =
            profiles.some(
                profile =>
                    Number(
                        profile.id
                    )
                    ===
                    Number(
                        detail.profile_id
                    )
            );

        if (profileExists) {
            selectGenerateProfile(
                detail.profile_id
            );
        } else {
            showToast(
                "The original workflow is archived. Choose an active workflow before generating."
            );
        }

        description.value =
            detail.description
            ||
            "";

        characterCount.textContent =
            `${description.value.length} characters`;

        setCreateOutputCount(
            detail.requested_count
            ||
            "auto"
        );

        const files = [];

        for (
            const reference
            of
            (
                detail.references
                ||
                []
            )
        ) {
            const response =
                await fetch(
                    reference.file_url
                );

            if (!response.ok) {
                throw new Error(
                    `Could not reload reference ${reference.position}.`
                );
            }

            const blob =
                await response.blob();

            const filename =
                reference.original_filename
                ||
                `reference-${reference.position}.jpg`;

            files.push(
                new File(
                    [
                        blob
                    ],
                    filename,
                    {
                        type:
                            blob.type
                            ||
                            "image/jpeg",
                    }
                )
            );
        }

        selectedImages =
            files;

        renderReferenceCards();

        closeModal(
            historyDetailModal
        );

        showView(
            "generate"
        );

        window.scrollTo({
            top:
                0,
            behavior:
                "smooth",
        });

        showToast(
            "Job loaded into Create. Current provider settings will be used for the new run."
        );

    } catch (error) {
        showToast(
            error.message
        );

    } finally {
        historyDuplicateButton.disabled =
            false;

        historyDuplicateButton.textContent =
            "Duplicate in Create";
    }
}


function setCreateOutputCount(
    value
) {
    const normalized =
        String(
            value
            ||
            "auto"
        );

    let found =
        false;

    document
        .querySelectorAll(
            ".count-button"
        )
        .forEach(
            button => {
                const selected =
                    button.dataset.count
                    ===
                    normalized;

                button.classList.toggle(
                    "selected",
                    selected
                );

                if (selected) {
                    found =
                        true;
                }
            }
        );

    selectedCount =
        found
            ?
            normalized
            :
            "auto";

    if (!found) {
        const auto =
            document.querySelector(
                '.count-button[data-count="auto"]'
            );

        if (auto) {
            auto.classList.add(
                "selected"
            );
        }
    }

    summaryCount.textContent =
        selectedCount
        ===
        "auto"
            ?
            "Auto"
            :
            selectedCount;

    updateCreateCostEstimate();
}


/* History filters */

historySearchInput.addEventListener(
    "input",
    () => {
        clearTimeout(
            historySearchTimer
        );

        historySearchTimer =
            setTimeout(
                loadHistory,
                280
            );
    }
);


[
    historyProfileFilter,
    historyStatusFilter,
    historyPlannerFilter,
    historyImageProviderFilter,
    historyFavoritesOnly,
].forEach(
    element => {
        element.addEventListener(
            "change",
            loadHistory
        );
    }
);


historyClearFiltersButton.addEventListener(
    "click",
    async () => {
        historySearchInput.value =
            "";

        historyProfileFilter.value =
            "";

        historyStatusFilter.value =
            "";

        historyPlannerFilter.value =
            "";

        historyImageProviderFilter.value =
            "";

        historyFavoritesOnly.checked =
            false;

        await loadHistory();
    }
);


historyEmptyCreateButton.addEventListener(
    "click",
    () => {
        showView(
            "generate"
        );

        window.scrollTo({
            top:
                0,
            behavior:
                "smooth",
        });
    }
);


/* =========================================================
   PROFILE MANAGER
========================================================= */

async function loadManagerProfiles() {
    try {
        const response =
            await fetch(
                "/api/profiles?include_archived=true"
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const data =
            await response.json();

        managerProfiles =
            Array.isArray(
                data.profiles
            )
                ?
                data.profiles
                :
                [];

        libraryCount.textContent =
            String(
                managerProfiles.length
            );

        renderManagerProfiles();

    } catch (error) {
        profileManagerList.innerHTML = `
            <div class="loading-state">
                Could not load profiles.
            </div>
        `;

        showToast(
            error.message
        );
    }
}


function renderManagerProfiles() {
    profileManagerList.innerHTML =
        "";

    const query =
        profileSearch
            .value
            .trim()
            .toLowerCase();

    const filtered =
        managerProfiles.filter(
            profile => {
                const value =
                    `${profile.name} ${profile.description || ""}`
                        .toLowerCase();

                return value.includes(
                    query
                );
            }
        );

    if (!filtered.length) {
        profileManagerList.innerHTML = `
            <div class="loading-state">
                No profiles found.
            </div>
        `;

        return;
    }

    filtered.forEach(
        profile => {
            const button =
                document.createElement(
                    "button"
                );

            button.type =
                "button";

            button.className =
                "manager-profile-item";

            if (
                Number(profile.id)
                ===
                Number(editingProfileId)
            ) {
                button.classList.add(
                    "selected"
                );
            }

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "manager-profile-title-row";

            const title =
                document.createElement(
                    "div"
                );

            title.className =
                "manager-profile-title";

            title.textContent =
                profile.name;

            row.appendChild(
                title
            );

            const desc =
                document.createElement(
                    "div"
                );

            desc.className =
                "manager-profile-description";

            desc.textContent =
                profile.description
                ||
                "No description";

            const status =
                document.createElement(
                    "span"
                );

            status.className =
                "manager-profile-status";

            status.textContent =
                Number(
                    profile.is_active
                )
                ===
                1
                    ?
                    "ACTIVE"
                    :
                    "ARCHIVED";

            button.append(
                row,
                desc,
                status
            );

            button.addEventListener(
                "click",
                () =>
                    openProfileEditor(
                        profile.id
                    )
            );

            profileManagerList.appendChild(
                button
            );
        }
    );
}


profileSearch.addEventListener(
    "input",
    renderManagerProfiles
);


async function openProfileEditor(
    profileId
) {
    try {
        const response =
            await fetch(
                `/api/profiles/${profileId}`
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const profile =
            await response.json();

        editingProfileId =
            Number(
                profile.id
            );

        editingProfileName =
            profile.name;

        profileEditorEmpty.classList.add(
            "hidden-element"
        );

        profileEditorContent.classList.remove(
            "hidden-element"
        );

        profileEditorTitle.textContent =
            profile.name;

        profileNameInput.value =
            profile.name;

        profileDescriptionInput.value =
            profile.description
            ||
            "";

        profileInstructionEditor.value =
            profile.system_instruction
            ||
            "";

        instructionCharacterCount.textContent =
            `${formatNumber(profileInstructionEditor.value.length)} characters`;

        const active =
            Number(
                profile.is_active
            )
            ===
            1;

        profileStateBadge.textContent =
            active
                ?
                "ACTIVE"
                :
                "ARCHIVED";

        archiveProfileButton.classList.toggle(
            "hidden-element",
            !active
        );

        restoreProfileButton.classList.toggle(
            "hidden-element",
            active
        );

        [
            profileNameInput,
            profileDescriptionInput,
            profileInstructionEditor,
            saveDetailsButton,
            saveVersionButton,
        ].forEach(
            item => {
                item.disabled =
                    !active;
            }
        );

        renderManagerProfiles();

    } catch (error) {
        showToast(
            error.message
        );
    }
}


profileInstructionEditor.addEventListener(
    "input",
    () => {
        instructionCharacterCount.textContent =
            `${formatNumber(profileInstructionEditor.value.length)} characters`;
    }
);


saveDetailsButton.addEventListener(
    "click",
    async () => {
        if (!editingProfileId) {
            return;
        }

        const name =
            profileNameInput
                .value
                .trim();

        if (!name) {
            showToast(
                "Profile name cannot be empty."
            );

            return;
        }

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}`,
                    {
                        method:
                            "PATCH",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                name:
                                    name,

                                description:
                                    profileDescriptionInput
                                        .value
                                        .trim(),
                            }),
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            await response.json();

            await loadProfiles(
                editingProfileId
            );

            await loadManagerProfiles();

            await openProfileEditor(
                editingProfileId
            );

            showToast(
                "Profile details saved."
            );

        } catch (error) {
            showToast(
                error.message
            );
        }
    }
);


saveVersionButton.addEventListener(
    "click",
    async () => {
        if (!editingProfileId) {
            return;
        }

        const instruction =
            profileInstructionEditor
                .value
                .trim();

        if (!instruction) {
            showToast(
                "System instruction cannot be empty."
            );

            return;
        }

        saveVersionButton.disabled =
            true;

        saveVersionButton.textContent =
            "Saving…";

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}/instruction`,
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                system_instruction:
                                    instruction
                            }),
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            await response.json();

            await loadProfiles(
                editingProfileId
            );

            await loadManagerProfiles();

            await openProfileEditor(
                editingProfileId
            );

            showToast(
                "Current system instruction updated."
            );

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            saveVersionButton.disabled =
                false;

            saveVersionButton.textContent =
                "Save instruction";
        }
    }
);


archiveProfileButton.addEventListener(
    "click",
    async () => {
        if (!editingProfileId) {
            return;
        }

        if (
            !window.confirm(
                `Archive "${editingProfileName}"?`
            )
        ) {
            return;
        }

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}`,
                    {
                        method: "DELETE"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            await response.json();

            const id =
                editingProfileId;

            await loadProfiles();
            await loadManagerProfiles();
            await openProfileEditor(
                id
            );

            showToast(
                "Profile archived."
            );

        } catch (error) {
            showToast(
                error.message
            );
        }
    }
);


restoreProfileButton.addEventListener(
    "click",
    async () => {
        if (!editingProfileId) {
            return;
        }

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}/restore`,
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            await response.json();

            const id =
                editingProfileId;

            await loadProfiles(
                id
            );

            await loadManagerProfiles();

            await openProfileEditor(
                id
            );

            showToast(
                "Profile restored."
            );

        } catch (error) {
            showToast(
                error.message
            );
        }
    }
);


deleteProfileButton.addEventListener(
    "click",
    async () => {
        if (!editingProfileId) {
            return;
        }

        const typed =
            window.prompt(
                `Type the profile name exactly to permanently delete it:\n\n${editingProfileName}`
            );

        if (
            typed
            !==
            editingProfileName
        ) {
            if (
                typed !== null
            ) {
                showToast(
                    "Profile name did not match."
                );
            }

            return;
        }

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}/permanent`,
                    {
                        method: "DELETE"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            await response.json();

            editingProfileId =
                null;

            editingProfileName =
                null;

            profileEditorContent.classList.add(
                "hidden-element"
            );

            profileEditorEmpty.classList.remove(
                "hidden-element"
            );

            await loadProfiles();
            await loadManagerProfiles();

            showToast(
                "Profile deleted."
            );

        } catch (error) {
            showToast(
                error.message
            );
        }
    }
);


/* =========================================================
   NEW PROFILE MODAL
========================================================= */

newProfileButton.addEventListener(
    "click",
    () => {
        newProfileForm.reset();

        newInstructionCharacterCount.textContent =
            "0 characters";

        openModal(
            newProfileModal
        );
    }
);


modalCloseButton.addEventListener(
    "click",
    () =>
        closeModal(
            newProfileModal
        )
);


cancelCreateProfile.addEventListener(
    "click",
    () =>
        closeModal(
            newProfileModal
        )
);


newProfileInstruction.addEventListener(
    "input",
    () => {
        newInstructionCharacterCount.textContent =
            `${formatNumber(newProfileInstruction.value.length)} characters`;
    }
);


newProfileForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const name =
            newProfileName
                .value
                .trim();

        const instruction =
            newProfileInstruction
                .value
                .trim();

        if (
            !name
            ||
            !instruction
        ) {
            showToast(
                "Name and system instruction are required."
            );

            return;
        }

        try {
            const response =
                await fetch(
                    "/api/profiles",
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                name:
                                    name,

                                description:
                                    newProfileDescription
                                        .value
                                        .trim(),

                                system_instruction:
                                    instruction,
                            }),
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            const profile =
                await response.json();

            closeModal(
                newProfileModal
            );

            await loadProfiles(
                profile.id
            );

            await loadManagerProfiles();

            await openProfileEditor(
                profile.id
            );

            showToast(
                "Profile created."
            );

        } catch (error) {
            showToast(
                error.message
            );
        }
    }
);


/* =========================================================
   MODALS
========================================================= */

function openModal(
    element
) {
    element.classList.add(
        "visible"
    );

    element.setAttribute(
        "aria-hidden",
        "false"
    );
}


function closeModal(
    element
) {
    element.classList.remove(
        "visible"
    );

    element.setAttribute(
        "aria-hidden",
        "true"
    );
}


[
    finalInputModal,
    imagePreviewModal,
    regenerateModal,
    compareModal,
    newProfileModal,
    historyDetailModal,
].forEach(
    modal => {
        modal.addEventListener(
            "click",
            event => {
                if (
                    event.target
                    ===
                    modal
                ) {
                    closeModal(
                        modal
                    );
                }
            }
        );
    }
);


closeFinalInputModal.addEventListener(
    "click",
    () =>
        closeModal(
            finalInputModal
        )
);


closeImagePreviewModal.addEventListener(
    "click",
    () =>
        closeModal(
            imagePreviewModal
        )
);


closeRegenerateModal.addEventListener(
    "click",
    () =>
        closeModal(
            regenerateModal
        )
);


cancelRegenerateButton.addEventListener(
    "click",
    () =>
        closeModal(
            regenerateModal
        )
);


closeCompareModal.addEventListener(
    "click",
    () =>
        closeModal(
            compareModal
        )
);


closeHistoryDetailModal.addEventListener(
    "click",
    () =>
        closeModal(
            historyDetailModal
        )
);


document.addEventListener(
    "keydown",
    event => {
        if (
            event.key
            ===
            "Escape"
        ) {
            [
                finalInputModal,
                imagePreviewModal,
                regenerateModal,
                compareModal,
                newProfileModal,
            ].forEach(
                closeModal
            );
        }

        if (
            imagePreviewModal
                .classList
                .contains(
                    "visible"
                )
        ) {
            if (
                event.key
                ===
                "ArrowLeft"
            ) {
                previewPreviousButton.click();
            }

            if (
                event.key
                ===
                "ArrowRight"
            ) {
                previewNextButton.click();
            }
        }
    }
);


/* =========================================================
   FORMAT / PROVIDER HELPERS
========================================================= */

function initials(
    name
) {
    const words =
        String(
            name
            ||
            ""
        )
        .trim()
        .split(/\s+/)
        .filter(Boolean);

    if (!words.length) {
        return "?";
    }

    if (
        words.length
        ===
        1
    ) {
        return words[0]
            .slice(
                0,
                2
            )
            .toUpperCase();
    }

    return (
        words[0][0]
        +
        words[1][0]
    ).toUpperCase();
}


function formatNumber(
    value
) {
    return Number(
        value
        ||
        0
    ).toLocaleString();
}


function capitalize(
    value
) {
    const string =
        String(
            value
            ||
            ""
        );

    return (
        string.charAt(0).toUpperCase()
        +
        string.slice(1)
    );
}


function providerLabel(
    value
) {
    const provider =
        String(
            value
            ||
            ""
        ).split(
            ":"
        )[0];

    return provider
        ?
        provider.toUpperCase()
        :
        "AI";
}


function providerMeta(
    value
) {
    const pieces =
        String(
            value
            ||
            ""
        ).split(
            ":"
        );

    if (!pieces.length) {
        return "AI provider";
    }

    return pieces
        .filter(Boolean)
        .map(
            (
                value,
                index
            ) =>
                index === 0
                    ?
                    value.toUpperCase()
                    :
                    value
        )
        .join(
            " · "
        );
}


/* =========================================================
   TOAST
========================================================= */

function showToast(
    message
) {
    clearTimeout(
        toastTimer
    );

    toast.textContent =
        message;

    toast.classList.add(
        "visible"
    );

    toastTimer =
        setTimeout(
            () => {
                toast.classList.remove(
                    "visible"
                );
            },
            3400
        );
}


/* =========================================================
   STARTUP
========================================================= */

async function startApplication() {
    showView(
        "generate"
    );

    await Promise.all([
        loadSettings(),
        loadProfiles(),
    ]);

    renderReferenceCards();
}


startApplication();
