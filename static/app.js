/* =========================================================
   HYPEREX — STEP 11 STUDIO UI
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
const navAdmin = $("navAdmin");

const generateView = $("generateView");
const profilesView = $("profilesView");
const historyView = $("historyView");
const settingsView = $("settingsView");
const adminView = $("adminView");

const authGate = $("authGate");
const appShell = $("appShell");
const authLoginTab = $("authLoginTab");
const authSignupTab = $("authSignupTab");
const authForm = $("authForm");
const authEmailInput = $("authEmailInput");
const authPasswordInput = $("authPasswordInput");
const authSubmitButton = $("authSubmitButton");
const authMessage = $("authMessage");
const authLocalNote = $("authLocalNote");
const authTabs = $("authTabs");
const forgotPasswordButton = $("forgotPasswordButton");
const forgotPasswordPanel = $("forgotPasswordPanel");
const forgotPasswordEmailInput = $("forgotPasswordEmailInput");
const sendPasswordResetButton = $("sendPasswordResetButton");
const forgotPasswordBackButton = $("forgotPasswordBackButton");
const forgotPasswordMessage = $("forgotPasswordMessage");

const verificationGate = $("verificationGate");
const verificationEmail = $("verificationEmail");
const verificationMessage = $("verificationMessage");
const checkVerificationButton = $("checkVerificationButton");
const resendVerificationButton = $("resendVerificationButton");
const verificationLogoutButton = $("verificationLogoutButton");

const sidebarUserEmail = $("sidebarUserEmail");
const settingsUserEmail = $("settingsUserEmail");
const logoutButton = $("logoutButton");
const claimLocalDataButton = $("claimLocalDataButton");
const localImportStatusText = $("localImportStatusText");
const accountSecurityEmail = $("accountSecurityEmail");
const accountVerificationBadge = $("accountVerificationBadge");
const changePasswordButton = $("changePasswordButton");

const refreshAdminButton = $("refreshAdminButton");
const adminUsersCount = $("adminUsersCount");
const adminJobsCount = $("adminJobsCount");
const adminJobsTodayCount = $("adminJobsTodayCount");
const adminImagesCount = $("adminImagesCount");
const adminSuccessRate = $("adminSuccessRate");
const adminWorkflowsCount = $("adminWorkflowsCount");
const adminSystemList = $("adminSystemList");
const adminModelList = $("adminModelList");
const adminUserList = $("adminUserList");
const adminFailureList = $("adminFailureList");

const addAdminWorkflowButton = $("addAdminWorkflowButton");
const adminPublishedWorkflowCount = $("adminPublishedWorkflowCount");
const adminDraftWorkflowCount = $("adminDraftWorkflowCount");
const adminPrivateWorkflowCount = $("adminPrivateWorkflowCount");
const adminTemplateWorkflowCount = $("adminTemplateWorkflowCount");
const adminWorkflowList = $("adminWorkflowList");

const createPlannerSummary = $("createPlannerSummary");
const createImageSummary = $("createImageSummary");
const createCostEstimate = $("createCostEstimate");
const openSettingsFromCreate = $("openSettingsFromCreate");

const profileOptions = $("profileOptions");
const newGenerationButton = $("newGenerationButton");

const imageInput = $("imageInput");
const replaceImageInput = $("replaceImageInput");
const uploadZone = $("uploadZone");
const imagePreviewGrid = $("imagePreviewGrid");

const description = $("description");
const characterCount = $("characterCount");

const autoGenerateImages = $("autoGenerateImages");
const ratioSelector = $("ratioSelector");

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
const summaryRatio = $("summaryRatio");
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
const customizeTemplateButton = $("customizeTemplateButton");
const privateProfileNotice = $("privateProfileNotice");


/* Settings */

const saveSettingsButton = $("saveSettingsButton");

const plannerProviderStatus = $("plannerProviderStatus");
const plannerProviderSelect = $("plannerProviderSelect");
const plannerModelSelect = $("plannerModelSelect");
const plannerTierChoices = $("plannerTierChoices");
const plannerResolvedModel = $("plannerResolvedModel");
const plannerTierNote = $("plannerTierNote");
const openaiReasoningField = $("openaiReasoningField");
const openaiReasoningSelect = $("openaiReasoningSelect");
const plannerConnectionSummary = $("plannerConnectionSummary");
const testPlannerButton = $("testPlannerButton");
const plannerTestResult = $("plannerTestResult");

const imageProviderStatus = $("imageProviderStatus");
const imageProviderSelect = $("imageProviderSelect");
const imageModelSelect = $("imageModelSelect");
const imageTierChoices = $("imageTierChoices");
const imageResolvedModel = $("imageResolvedModel");
const imageTierNote = $("imageTierNote");
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

const openaiApiKeyInput = $("openaiApiKeyInput");
const geminiApiKeyInput = $("geminiApiKeyInput");
const saveOpenaiKeyButton = $("saveOpenaiKeyButton");
const saveGeminiKeyButton = $("saveGeminiKeyButton");
const removeOpenaiKeyButton = $("removeOpenaiKeyButton");
const removeGeminiKeyButton = $("removeGeminiKeyButton");
const openaiKeyConnectionText = $("openaiKeyConnectionText");
const geminiKeyConnectionText = $("geminiKeyConnectionText");
const providerKeyResult = $("providerKeyResult");

const confirmBatchOverSelect = $("confirmBatchOverSelect");
const maxOutputCountSelect = $("maxOutputCountSelect");
const draftAutosaveCheckbox = $("draftAutosaveCheckbox");


/* Admin Workflow Modal */

const adminWorkflowModal = $("adminWorkflowModal");
const closeAdminWorkflowModal = $("closeAdminWorkflowModal");
const adminWorkflowModalTitle = $("adminWorkflowModalTitle");
const adminWorkflowNameInput = $("adminWorkflowNameInput");
const adminWorkflowSortOrderInput = $("adminWorkflowSortOrderInput");
const adminWorkflowDescriptionInput = $("adminWorkflowDescriptionInput");
const adminWorkflowPrivateType = $("adminWorkflowPrivateType");
const adminWorkflowTemplateType = $("adminWorkflowTemplateType");
const adminWorkflowInstructionInput = $("adminWorkflowInstructionInput");
const adminWorkflowSecurityTitle = $("adminWorkflowSecurityTitle");
const adminWorkflowSecurityText = $("adminWorkflowSecurityText");
const adminWorkflowVersionPanel = $("adminWorkflowVersionPanel");
const adminWorkflowVersionList = $("adminWorkflowVersionList");
const duplicateAdminWorkflowButton = $("duplicateAdminWorkflowButton");
const unpublishAdminWorkflowButton = $("unpublishAdminWorkflowButton");
const archiveAdminWorkflowButton = $("archiveAdminWorkflowButton");
const deleteAdminWorkflowButton = $("deleteAdminWorkflowButton");
const cancelAdminWorkflowButton = $("cancelAdminWorkflowButton");
const saveAdminWorkflowDraftButton = $("saveAdminWorkflowDraftButton");
const publishAdminWorkflowButton = $("publishAdminWorkflowButton");
const adminWorkflowFormMessage = $("adminWorkflowFormMessage");


/* Change Password Modal */

const changePasswordModal = $("changePasswordModal");
const closeChangePasswordModal = $("closeChangePasswordModal");
const cancelChangePasswordButton = $("cancelChangePasswordButton");
const changePasswordSubmitButton = $("changePasswordSubmitButton");
const newPasswordInput = $("newPasswordInput");
const confirmNewPasswordInput = $("confirmNewPasswordInput");
const changePasswordMessage = $("changePasswordMessage");


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
const historyDetailRatio = $("historyDetailRatio");
const historyDetailReferenceCount = $("historyDetailReferenceCount");
const historyDetailReferences = $("historyDetailReferences");
const historyDetailDirection = $("historyDetailDirection");
const historyDetailImageCount = $("historyDetailImageCount");
const historyDetailImages = $("historyDetailImages");
const historyDetailPrompts = $("historyDetailPrompts");
const historyDeleteJobButton = $("historyDeleteJobButton");

const mobileBottomNav = $("mobileBottomNav");
const mobileNavCreate = $("mobileNavCreate");
const mobileNavProfiles = $("mobileNavProfiles");
const mobileNavHistory = $("mobileNavHistory");
const mobileNavSettings = $("mobileNavSettings");
const mobileNavAdmin = $("mobileNavAdmin");
const mobileGenerateButton = $("mobileGenerateButton");
const mobileGenerateDock = $("mobileGenerateDock");

const toast = $("toast");


/* =========================================================
   STATE
========================================================= */

let profiles = [];
let managerProfiles = [];

let authProvider = "local";
let currentUser = null;
let authFormMode = "login";
let applicationStarted = false;
let verificationCooldownTimer = null;
let passwordResetCooldownTimer = null;

let selectedProfileId = null;
let selectedProfileVersionId = null;

let selectedImages = [];
let replaceTargetIndex = null;
let draggedReferenceIndex = null;

let selectedCount = "auto";
let selectedAspectRatio = "1:1";

let editingProfileId = null;
let editingProfileName = null;

let currentJob = null;
let currentPromptPackages = [];
let activeFinalPackage = null;

let settingsPayload = null;
let providerConnections = null;
let providerConnectionsLoadedAt = 0;

const CREATE_DRAFT_KEY =
    "hyperexCreateDraftV1";

const LAST_JOB_KEY =
    "hyperexLastJobV1";

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

let adminWorkflows = [];
let editingAdminWorkflowId = null;
let editingAdminWorkflowStatus = null;
let editingAdminWorkflowSystem = false;

let regenerateTarget = null;
let regenerateJobId = null;

let advancedOpen = false;

let toastTimer = null;


function isBuiltinProfile(
    profile
) {
    return Boolean(
        profile
        &&
        profile.is_builtin
    );
}


function isManagedProfile(
    profile
) {
    return Boolean(
        profile
        &&
        profile.is_managed
    );
}


function workflowTypeLabel(
    profile
) {
    if (
        profile?.workflow_type
        ===
        "template"
    ) {
        return "PUBLIC TEMPLATE";
    }

    if (
        profile?.workflow_type
        ===
        "private"
    ) {
        return "PRIVATE WORKFLOW";
    }

    return "MY PROFILE";
}


function setSelectedAspectRatio(
    ratio
) {
    selectedAspectRatio =
        ratio
        ||
        "1:1";

    document
        .querySelectorAll(
            ".ratio-button"
        )
        .forEach(
            button => {
                button.classList.toggle(
                    "selected",
                    button.dataset.ratio
                    ===
                    selectedAspectRatio
                );
            }
        );

    if (summaryRatio) {
        summaryRatio.textContent =
            selectedAspectRatio;
    }
}


if (ratioSelector) {
    ratioSelector.addEventListener(
        "click",
        event => {
            const button =
                event.target.closest(
                    ".ratio-button"
                );

            if (!button) {
                return;
            }

            setSelectedAspectRatio(
                button.dataset.ratio
            );

            saveCreateDraft();
        }
    );
}


/* =========================================================
   CREATE DRAFT / RECOVERY
========================================================= */

function autosaveEnabled() {
    return (
        settingsPayload
            ?.settings
            ?.draft_autosave
        !==
        false
    );
}


function saveCreateDraft() {
    if (!autosaveEnabled()) {
        return;
    }

    const payload = {
        profile_id:
            selectedProfileId,
        description:
            description.value,
        requested_count:
            selectedCount,
        aspect_ratio:
            selectedAspectRatio,
        auto_generate:
            autoGenerateImages.checked,
        saved_at:
            new Date().toISOString(),
    };

    localStorage.setItem(
        CREATE_DRAFT_KEY,
        JSON.stringify(
            payload
        )
    );
}


function restoreCreateDraft() {
    if (!autosaveEnabled()) {
        return false;
    }

    const raw =
        localStorage.getItem(
            CREATE_DRAFT_KEY
        );

    if (!raw) {
        return false;
    }

    try {
        const draft =
            JSON.parse(
                raw
            );

        if (
            draft.profile_id
            &&
            profiles.some(
                profile =>
                    Number(
                        profile.id
                    )
                    ===
                    Number(
                        draft.profile_id
                    )
            )
        ) {
            selectGenerateProfile(
                draft.profile_id,
                false
            );
        }

        description.value =
            draft.description
            ||
            "";

        characterCount.textContent =
            `${description.value.length} characters`;

        setCreateOutputCount(
            draft.requested_count
            ||
            "auto",
            false
        );

        setSelectedAspectRatio(
            draft.aspect_ratio
            ||
            "1:1"
        );

        autoGenerateImages.checked =
            draft.auto_generate
            !==
            false;

        return true;

    } catch {
        return false;
    }
}


function shouldConfirmGeneration() {
    if (!settingsPayload) {
        return false;
    }

    const settings =
        settingsPayload.settings;

    const count =
        selectedCount
        ===
        "auto"
            ?
            null
            :
            Number(
                selectedCount
            );

    const threshold =
        Number(
            settings.confirm_batch_over
            ||
            4
        );

    const highQuality =
        settings.image_provider
        ===
        "openai"
        &&
        settings.openai_image_quality
        ===
        "high";

    return (
        (
            count
            &&
            count > threshold
        )
        ||
        highQuality
    );
}


function confirmGenerationSafety() {
    if (!shouldConfirmGeneration()) {
        return true;
    }

    const provider =
        settingsPayload.settings
            .image_provider
            .toUpperCase();

    const quality =
        settingsPayload.settings
            .image_provider
        ===
        "openai"
            ?
            ` · ${capitalize(settingsPayload.settings.openai_image_quality)}`
            :
            "";

    const count =
        selectedCount
        ===
        "auto"
            ?
            "Auto"
            :
            selectedCount;

    return window.confirm(
        `Generate ${count} output(s) with ${provider}${quality}?\n\n`
        +
        "This may use paid provider credits."
    );
}


async function restoreLastJob() {
    const raw =
        localStorage.getItem(
            LAST_JOB_KEY
        );

    const jobId =
        Number(
            raw
        );

    if (!jobId) {
        return false;
    }

    try {
        const [
            jobResponse,
            batchResponse,
        ] =
            await Promise.all([
                fetch(
                    `/api/jobs/${jobId}`
                ),
                fetch(
                    `/api/jobs/${jobId}/image-batch`
                ),
            ]);

        if (!jobResponse.ok) {
            localStorage.removeItem(
                LAST_JOB_KEY
            );

            return false;
        }

        const job =
            await jobResponse.json();

        const batch =
            batchResponse.ok
                ?
                await batchResponse.json()
                :
                null;

        const finishedStatuses =
            new Set([
                "complete",
                "partial_failed",
                "failed",
            ]);

        /*
         * A completed job belongs in History.
         * Do not automatically reopen it every time the user starts Hyperex.
         *
         * We still restore unfinished/running jobs so refresh recovery remains.
         */
        if (
            batch
            &&
            finishedStatuses.has(
                String(
                    batch.status
                    ||
                    ""
                ).toLowerCase()
            )
        ) {
            localStorage.removeItem(
                LAST_JOB_KEY
            );

            return false;
        }

        currentJob =
            job;

        renderPreparedJob(
            currentJob
        );

        showPipeline(
            currentJob.id
        );

        setPipelineStep(
            pipelineReferences,
            "complete",
            `${currentJob.reference_count || 0} saved`
        );

        if (
            currentJob.planner_raw_output
        ) {
            renderPlannerResult(
                currentJob
            );

            setPipelineStep(
                pipelinePlanner,
                "complete",
                "Plan ready"
            );
        }

        const packageResponse =
            await fetch(
                `/api/jobs/${jobId}/packages`
            );

        if (
            packageResponse.ok
        ) {
            const packages =
                await packageResponse.json();

            if (
                packages.source_verified
            ) {
                renderPromptPackages(
                    packages
                );

                setPipelineStep(
                    pipelineVerify,
                    "complete",
                    `${packages.package_count} verified`
                );
            }
        }

        if (batch) {
            renderImageBatch(
                batch
            );

            if (
                batch.status
                ===
                "generating"
                ||
                batch.status
                ===
                "queued"
            ) {
                setPipelineStep(
                    pipelineImages,
                    "active",
                    "Running / reconnecting"
                );

                startImageBatchPolling(
                    jobId
                );
            }
        }

        return true;

    } catch (error) {
        console.warn(
            "Last-job recovery skipped:",
            error
        );

        return false;
    }
}


/* =========================================================
   AUTHENTICATION
========================================================= */

function setAuthMessage(
    message,
    state = ""
) {
    authMessage.textContent =
        message;

    authMessage.className =
        "auth-message";

    if (state) {
        authMessage.classList.add(
            state
        );
    }
}


function setForgotPasswordMessage(
    message,
    state = ""
) {
    forgotPasswordMessage.textContent =
        message;

    forgotPasswordMessage.className =
        "auth-message";

    if (state) {
        forgotPasswordMessage.classList.add(
            state
        );
    }
}


function setVerificationMessage(
    message,
    state = ""
) {
    verificationMessage.textContent =
        message;

    verificationMessage.className =
        "auth-message";

    if (state) {
        verificationMessage.classList.add(
            state
        );
    }
}


function setAuthFormMode(
    mode
) {
    authFormMode =
        mode
        ===
        "signup"
            ?
            "signup"
            :
            "login";

    authLoginTab.classList.toggle(
        "active",
        authFormMode
        ===
        "login"
    );

    authSignupTab.classList.toggle(
        "active",
        authFormMode
        ===
        "signup"
    );

    authSubmitButton.textContent =
        authFormMode
        ===
        "login"
            ?
            "SIGN IN →"
            :
            "CREATE ACCOUNT →";

    authPasswordInput.autocomplete =
        authFormMode
        ===
        "login"
            ?
            "current-password"
            :
            "new-password";

    forgotPasswordButton.classList.toggle(
        "hidden-element",
        authFormMode
        !==
        "login"
    );

    setAuthMessage(
        authFormMode
        ===
        "login"
            ?
            "Sign in to continue."
            :
            "Create your account, then verify your email before using Hyperex."
    );
}


function showForgotPasswordPanel() {
    const email =
        authEmailInput
            .value
            .trim();

    forgotPasswordEmailInput.value =
        email;

    authTabs.classList.add(
        "hidden-element"
    );

    authForm.classList.add(
        "hidden-element"
    );

    authMessage.classList.add(
        "hidden-element"
    );

    forgotPasswordPanel.classList.remove(
        "hidden-element"
    );

    setForgotPasswordMessage(
        "Enter your email and we'll send secure reset instructions."
    );

    requestAnimationFrame(
        () =>
            forgotPasswordEmailInput.focus()
    );
}


function hideForgotPasswordPanel() {
    forgotPasswordPanel.classList.add(
        "hidden-element"
    );

    authTabs.classList.remove(
        "hidden-element"
    );

    authForm.classList.remove(
        "hidden-element"
    );

    authMessage.classList.remove(
        "hidden-element"
    );

    setAuthFormMode(
        "login"
    );
}


function startButtonCooldown(
    button,
    seconds,
    normalLabel,
    timerName
) {
    const duration =
        Math.max(
            1,
            Number(
                seconds
                ||
                60
            )
        );

    if (
        timerName
        ===
        "verification"
        &&
        verificationCooldownTimer
    ) {
        clearInterval(
            verificationCooldownTimer
        );
    }

    if (
        timerName
        ===
        "reset"
        &&
        passwordResetCooldownTimer
    ) {
        clearInterval(
            passwordResetCooldownTimer
        );
    }

    let remaining =
        duration;

    button.disabled =
        true;

    const render =
        () => {
            button.textContent =
                `${normalLabel} · ${remaining}s`;

            remaining -=
                1;

            if (
                remaining < 0
            ) {
                if (
                    timerName
                    ===
                    "verification"
                    &&
                    verificationCooldownTimer
                ) {
                    clearInterval(
                        verificationCooldownTimer
                    );

                    verificationCooldownTimer =
                        null;
                }

                if (
                    timerName
                    ===
                    "reset"
                    &&
                    passwordResetCooldownTimer
                ) {
                    clearInterval(
                        passwordResetCooldownTimer
                    );

                    passwordResetCooldownTimer =
                        null;
                }

                button.disabled =
                    false;

                button.textContent =
                    normalLabel;
            }
        };

    render();

    const timer =
        setInterval(
            render,
            1000
        );

    if (
        timerName
        ===
        "verification"
    ) {
        verificationCooldownTimer =
            timer;
    } else {
        passwordResetCooldownTimer =
            timer;
    }
}


function renderAuthenticatedUser() {
    const email =
        currentUser?.email
        ||
        (
            authProvider
            ===
            "local"
                ?
                "Local development"
                :
                "Signed in"
        );

    sidebarUserEmail.textContent =
        email;

    settingsUserEmail.textContent =
        email;

    accountSecurityEmail.textContent =
        email;

    const verified =
        authProvider
        ===
        "local"
        ||
        currentUser?.email_verified
        ===
        true;

    accountVerificationBadge.textContent =
        authProvider
        ===
        "local"
            ?
            "LOCAL MODE"
            :
            verified
                ?
                "VERIFIED"
                :
                "VERIFY EMAIL";

    accountVerificationBadge.classList.toggle(
        "verified",
        verified
    );

    accountVerificationBadge.classList.toggle(
        "warning",
        !verified
    );

    changePasswordButton.classList.toggle(
        "hidden-element",
        authProvider
        ===
        "local"
    );

    logoutButton.classList.toggle(
        "hidden-element",
        authProvider
        ===
        "local"
    );

    // Old pre-Firebase data migration is an admin-only maintenance action.
    // Keep it hidden until the backend confirms there is importable data.
    claimLocalDataButton.classList.add(
        "hidden-element"
    );

    localImportStatusText.classList.add(
        "hidden-element"
    );

    const isAdmin =
        currentUser?.role
        ===
        "admin";

    navAdmin.classList.toggle(
        "hidden-element",
        !isAdmin
    );

    if (mobileNavAdmin) {
        mobileNavAdmin.classList.toggle(
            "hidden-element",
            !isAdmin
        );
    }

    if (mobileBottomNav) {
        mobileBottomNav.classList.toggle(
            "admin-mode",
            isAdmin
        );
    }

    if (
        isAdmin
        &&
        authProvider
        !==
        "local"
    ) {
        void loadLocalImportStatus();
    }
}


function showAuthenticatedApp() {
    authGate.classList.add(
        "hidden-element"
    );

    verificationGate.classList.add(
        "hidden-element"
    );

    appShell.classList.remove(
        "hidden-element"
    );

    renderAuthenticatedUser();
}


function showAuthGate() {
    appShell.classList.add(
        "hidden-element"
    );

    verificationGate.classList.add(
        "hidden-element"
    );

    authGate.classList.remove(
        "hidden-element"
    );

    hideForgotPasswordPanel();
}


function showVerificationGate() {
    appShell.classList.add(
        "hidden-element"
    );

    authGate.classList.add(
        "hidden-element"
    );

    verificationGate.classList.remove(
        "hidden-element"
    );

    verificationEmail.textContent =
        currentUser?.email
        ||
        "your email";

    setVerificationMessage(
        "Open the verification email, click the link, then return here."
    );
}


async function getAuthSession() {
    try {
        const response =
            await fetch(
                "/api/auth/session",
                {
                    cache:
                        "no-store",
                }
            );

        if (!response.ok) {
            return {
                authenticated:
                    false,
                provider:
                    "firebase",
                user:
                    null,
            };
        }

        return await response.json();

    } catch {
        return {
            authenticated:
                false,
            provider:
                "firebase",
            user:
                null,
        };
    }
}


async function bootApplication() {
    const session =
        await getAuthSession();

    authProvider =
        session.provider
        ||
        "local";

    currentUser =
        session.user
        ||
        null;

    if (
        !session.authenticated
    ) {
        showAuthGate();
        setAuthFormMode(
            "login"
        );

        return;
    }

    if (
        authProvider
        ===
        "firebase"
        &&
        currentUser?.email_verified
        !==
        true
    ) {
        showVerificationGate();

        return;
    }

    showAuthenticatedApp();

    if (
        authProvider
        ===
        "local"
    ) {
        authLocalNote.classList.remove(
            "hidden-element"
        );
    }

    if (!applicationStarted) {
        applicationStarted =
            true;

        await startApplication();
    }
}


async function logoutAndReload() {
    try {
        await fetch(
            "/api/auth/logout",
            {
                method:
                    "POST",
            }
        );
    } finally {
        window.location.reload();
    }
}


authLoginTab.addEventListener(
    "click",
    () =>
        setAuthFormMode(
            "login"
        )
);


authSignupTab.addEventListener(
    "click",
    () =>
        setAuthFormMode(
            "signup"
        )
);


forgotPasswordButton.addEventListener(
    "click",
    showForgotPasswordPanel
);


forgotPasswordBackButton.addEventListener(
    "click",
    hideForgotPasswordPanel
);


sendPasswordResetButton.addEventListener(
    "click",
    async () => {
        const email =
            forgotPasswordEmailInput
                .value
                .trim();

        if (!email) {
            setForgotPasswordMessage(
                "Enter your email address.",
                "error"
            );

            return;
        }

        sendPasswordResetButton.disabled =
            true;

        sendPasswordResetButton.textContent =
            "SENDING…";

        try {
            const response =
                await fetch(
                    "/api/auth/password-reset",
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body:
                            JSON.stringify({
                                email:
                                    email,
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

            const result =
                await response.json();

            setForgotPasswordMessage(
                result.message
                ||
                (
                    "If an account exists for that email, "
                    +
                    "password reset instructions have been sent."
                ),
                "success"
            );

            startButtonCooldown(
                sendPasswordResetButton,
                result.retry_after
                ||
                60,
                "SEND RESET LINK →",
                "reset"
            );

        } catch (error) {
            sendPasswordResetButton.disabled =
                false;

            sendPasswordResetButton.textContent =
                "SEND RESET LINK →";

            setForgotPasswordMessage(
                error.message,
                "error"
            );
        }
    }
);


authForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const email =
            authEmailInput
            .value
            .trim();

        const password =
            authPasswordInput
            .value;

        if (
            !email
            ||
            password.length < 6
        ) {
            setAuthMessage(
                "Enter a valid email and a password of at least 6 characters.",
                "error"
            );

            return;
        }

        authSubmitButton.disabled =
            true;

        authSubmitButton.textContent =
            authFormMode
            ===
            "login"
                ?
                "SIGNING IN…"
                :
                "CREATING…";

        try {
            const endpoint =
                authFormMode
                ===
                "login"
                    ?
                    "/api/auth/login"
                    :
                    "/api/auth/signup";

            const response =
                await fetch(
                    endpoint,
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body:
                            JSON.stringify({
                                email:
                                    email,
                                password:
                                    password,
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

            const result =
                await response.json();

            if (
                result.needs_confirmation
                &&
                result.verification_sent
            ) {
                startButtonCooldown(
                    resendVerificationButton,
                    60,
                    "Resend verification email",
                    "verification"
                );
            }

            await bootApplication();

        } catch (error) {
            setAuthMessage(
                error.message,
                "error"
            );

        } finally {
            authSubmitButton.disabled =
                false;

            authSubmitButton.textContent =
                authFormMode
                ===
                "login"
                    ?
                    "SIGN IN →"
                    :
                    "CREATE ACCOUNT →";
        }
    }
);


checkVerificationButton.addEventListener(
    "click",
    async () => {
        checkVerificationButton.disabled =
            true;

        checkVerificationButton.textContent =
            "CHECKING…";

        try {
            const session =
                await getAuthSession();

            if (
                session.authenticated
                &&
                session.user?.email_verified
                ===
                true
            ) {
                setVerificationMessage(
                    "Email verified. Opening Hyperex…",
                    "success"
                );

                await bootApplication();

                return;
            }

            setVerificationMessage(
                "Not verified yet. Open the email link first, then check again.",
                "error"
            );

        } finally {
            checkVerificationButton.disabled =
                false;

            checkVerificationButton.textContent =
                "I'VE VERIFIED MY EMAIL →";
        }
    }
);


resendVerificationButton.addEventListener(
    "click",
    async () => {
        resendVerificationButton.disabled =
            true;

        resendVerificationButton.textContent =
            "SENDING…";

        try {
            const response =
                await fetch(
                    "/api/auth/verification/resend",
                    {
                        method:
                            "POST",
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

            if (
                result.already_verified
            ) {
                await bootApplication();

                return;
            }

            if (
                result.cooldown
            ) {
                setVerificationMessage(
                    "A verification email was already sent. Check your inbox and spam folder.",
                    "success"
                );
            } else {
                setVerificationMessage(
                    "Verification email sent. Check your inbox and spam folder.",
                    "success"
                );
            }

            startButtonCooldown(
                resendVerificationButton,
                result.retry_after
                ||
                60,
                "Resend verification email",
                "verification"
            );

        } catch (error) {
            resendVerificationButton.disabled =
                false;

            resendVerificationButton.textContent =
                "Resend verification email";

            setVerificationMessage(
                error.message,
                "error"
            );
        }
    }
);


verificationLogoutButton.addEventListener(
    "click",
    logoutAndReload
);


logoutButton.addEventListener(
    "click",
    logoutAndReload
);


function localImportSummary(
    counts
) {
    const safe =
        counts
        ||
        {};

    const parts =
        [];

    const profiles =
        Number(
            safe.profiles
            ||
            0
        );

    const jobs =
        Number(
            safe.jobs
            ||
            0
        );

    const images =
        Number(
            safe.images
            ||
            0
        );

    const providerConnections =
        Number(
            safe.provider_connections
            ||
            0
        );

    if (profiles) {
        parts.push(
            `${profiles} profile${profiles === 1 ? "" : "s"}`
        );
    }

    if (jobs) {
        parts.push(
            `${jobs} job${jobs === 1 ? "" : "s"}`
        );
    }

    if (images) {
        parts.push(
            `${images} generated image${images === 1 ? "" : "s"}`
        );
    }

    if (providerConnections) {
        parts.push(
            `${providerConnections} saved provider connection${providerConnections === 1 ? "" : "s"}`
        );
    }

    return (
        parts.join(
            " · "
        )
        ||
        "old local account data"
    );
}


async function loadLocalImportStatus() {
    claimLocalDataButton.classList.add(
        "hidden-element"
    );

    localImportStatusText.classList.add(
        "hidden-element"
    );

    if (
        authProvider
        ===
        "local"
        ||
        currentUser?.role
        !==
        "admin"
    ) {
        return null;
    }

    try {
        const response =
            await fetch(
                "/api/account/local-import-status",
                {
                    cache:
                        "no-store",
                }
            );

        if (!response.ok) {
            if (
                response.status
                ===
                403
            ) {
                return null;
            }

            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const status =
            await response.json();

        localImportStatusText.classList.remove(
            "hidden-element"
        );

        if (
            status.completed
        ) {
            localImportStatusText.textContent =
                "Old local data was already imported. This migration is closed.";

            return status;
        }

        if (
            status.available
        ) {
            localImportStatusText.textContent =
                (
                    "Admin-only migration available · "
                    +
                    localImportSummary(
                        status.counts
                    )
                );

            claimLocalDataButton.classList.remove(
                "hidden-element"
            );

            return status;
        }

        localImportStatusText.textContent =
            "No old local data is waiting to be imported.";

        return status;

    } catch (error) {
        console.warn(
            "Local import status check failed:",
            error
        );

        return null;
    }
}


claimLocalDataButton.addEventListener(
    "click",
    async () => {
        claimLocalDataButton.disabled =
            true;

        try {
            const status =
                await loadLocalImportStatus();

            if (
                !status
                ||
                !status.available
            ) {
                showToast(
                    status?.completed
                        ?
                        "Old local data was already imported."
                        :
                        "There is no old local data available to import."
                );

                return;
            }

            const summary =
                localImportSummary(
                    status.counts
                );

            const confirmed =
                window.confirm(
                    (
                        "Import the old pre-Firebase local data into THIS admin account?\n\n"
                        +
                        `${summary}\n\n`
                        +
                        "This includes old custom profiles, jobs/history, favorites, "
                        +
                        "saved Settings and encrypted provider connections.\n\n"
                        +
                        "Hero and UGC built-in workflows are not moved.\n\n"
                        +
                        "If this admin account already has matching Settings or saved "
                        +
                        "provider keys, the old local values will replace them.\n\n"
                        +
                        "This is a one-time migration and cannot be claimed by another user afterward."
                    )
                );

            if (!confirmed) {
                return;
            }

            const response =
                await fetch(
                    "/api/account/claim-local-data",
                    {
                        method:
                            "POST",
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

            if (
                result.claimed
            ) {
                localImportStatusText.classList.remove(
                    "hidden-element"
                );

                localImportStatusText.textContent =
                    "Old local data imported successfully. This migration is now closed.";

                claimLocalDataButton.classList.add(
                    "hidden-element"
                );

                providerConnections =
                    null;

                providerConnectionsLoadedAt =
                    0;

                showToast(
                    "Old local data moved into this admin account."
                );

                await Promise.all([
                    loadProfiles(),
                    loadManagerProfiles(),
                    loadHistory(),
                    loadSettings(),
                    loadProviderConnections(
                        true
                    ),
                ]);

            } else {
                await loadLocalImportStatus();

                showToast(
                    result.reason
                    ===
                    "already_completed"
                        ?
                        "Old local data was already imported."
                        :
                        "There was no old local data to import."
                );
            }

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            claimLocalDataButton.disabled =
                false;
        }
    }
);


changePasswordButton.addEventListener(
    "click",
    () => {
        newPasswordInput.value =
            "";

        confirmNewPasswordInput.value =
            "";

        changePasswordMessage.textContent =
            "Use at least 8 characters and avoid reusing another password.";

        openModal(
            changePasswordModal
        );

        requestAnimationFrame(
            () =>
                newPasswordInput.focus()
        );
    }
);


changePasswordSubmitButton.addEventListener(
    "click",
    async () => {
        const password =
            newPasswordInput.value;

        const confirmation =
            confirmNewPasswordInput.value;

        if (
            password.length < 8
        ) {
            changePasswordMessage.textContent =
                "Use at least 8 characters.";

            return;
        }

        if (
            password
            !==
            confirmation
        ) {
            changePasswordMessage.textContent =
                "The passwords do not match.";

            return;
        }

        changePasswordSubmitButton.disabled =
            true;

        changePasswordSubmitButton.textContent =
            "UPDATING…";

        try {
            const response =
                await fetch(
                    "/api/auth/change-password",
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body:
                            JSON.stringify({
                                new_password:
                                    password,
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
                changePasswordModal
            );

            newPasswordInput.value =
                "";

            confirmNewPasswordInput.value =
                "";

            showToast(
                "Password updated."
            );

        } catch (error) {
            changePasswordMessage.textContent =
                error.message;

        } finally {
            changePasswordSubmitButton.disabled =
                false;

            changePasswordSubmitButton.textContent =
                "Update password";
        }
    }
);


/* =========================================================
   ADMIN DASHBOARD
========================================================= */

async function loadAdminDashboard() {
    if (
        currentUser?.role
        !==
        "admin"
    ) {
        return;
    }

    try {
        const response =
            await fetch(
                "/api/admin/dashboard",
                {
                    cache:
                        "no-store",
                }
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

        adminWorkflows =
            Array.isArray(
                data.workflows
            )
                ?
                data.workflows
                :
                [];

        renderAdminOverview(
            data.overview
            ||
            {}
        );

        renderAdminWorkflowSummary(
            data.workflow_summary
            ||
            {}
        );

        renderAdminWorkflows(
            adminWorkflows
        );

        renderAdminUsers(
            data.users
            ||
            []
        );

        renderAdminModels(
            data.models
            ||
            []
        );

        renderAdminSystem(
            data.system
            ||
            {}
        );

        renderAdminFailures(
            data.recent_failures
            ||
            []
        );

    } catch (error) {
        showToast(
            error.message
        );
    }
}


function renderAdminOverview(
    overview
) {
    adminUsersCount.textContent =
        formatNumber(
            overview.users
            ||
            0
        );

    adminJobsCount.textContent =
        formatNumber(
            overview.jobs
            ||
            0
        );

    adminJobsTodayCount.textContent =
        formatNumber(
            overview.jobs_today
            ||
            0
        );

    adminImagesCount.textContent =
        formatNumber(
            overview.complete_images
            ||
            0
        );

    adminWorkflowsCount.textContent =
        formatNumber(
            overview.workflows
            ||
            0
        );

    adminSuccessRate.textContent =
        `${Number(
            overview.success_rate
            ??
            100
        ).toFixed(1)}%`;
}


function renderAdminWorkflowSummary(
    summary
) {
    adminPublishedWorkflowCount.textContent =
        formatNumber(
            summary.published
            ||
            0
        );

    adminDraftWorkflowCount.textContent =
        formatNumber(
            summary.drafts
            ||
            0
        );

    adminPrivateWorkflowCount.textContent =
        formatNumber(
            summary.private
            ||
            0
        );

    adminTemplateWorkflowCount.textContent =
        formatNumber(
            summary.templates
            ||
            0
        );
}


function adminWorkflowTypeLabel(
    workflow
) {
    return (
        workflow.workflow_type
        ===
        "template"
            ?
            "Public Template"
            :
            "Private Workflow"
    );
}


function adminWorkflowStatusLabel(
    status
) {
    const value =
        String(
            status
            ||
            ""
        ).toLowerCase();

    if (
        value
        ===
        "published"
    ) {
        return "Published";
    }

    if (
        value
        ===
        "unpublished"
    ) {
        return "Unpublished";
    }

    if (
        value
        ===
        "archived"
    ) {
        return "Archived";
    }

    return "Draft";
}


function renderAdminWorkflows(
    workflows
) {
    adminWorkflowList.innerHTML =
        "";

    if (!workflows.length) {
        adminWorkflowList.innerHTML = `
            <div class="admin-workflow-empty">
                <strong>No managed workflows yet.</strong>
                <span>Create your first workflow and publish it when ready.</span>
            </div>
        `;

        return;
    }

    workflows.forEach(
        workflow => {
            const row =
                document.createElement(
                    "article"
                );

            row.className =
                "admin-workflow-row";

            row.dataset.status =
                workflow.status
                ||
                "draft";

            row.dataset.type =
                workflow.workflow_type
                ||
                "private";

            const identity =
                document.createElement(
                    "div"
                );

            identity.className =
                "admin-workflow-identity";

            const titleRow =
                document.createElement(
                    "div"
                );

            titleRow.className =
                "admin-workflow-title-row";

            const title =
                document.createElement(
                    "strong"
                );

            title.textContent =
                workflow.name;

            const typeBadge =
                document.createElement(
                    "span"
                );

            typeBadge.className =
                `admin-workflow-type-badge ${
                    workflow.workflow_type
                    ===
                    "template"
                        ?
                        "template"
                        :
                        "private"
                }`;

            typeBadge.textContent =
                adminWorkflowTypeLabel(
                    workflow
                );

            titleRow.append(
                title,
                typeBadge
            );

            if (
                workflow.is_system
            ) {
                const systemBadge =
                    document.createElement(
                        "span"
                    );

                systemBadge.className =
                    "admin-workflow-system-badge";

                systemBadge.textContent =
                    "SYSTEM";

                titleRow.appendChild(
                    systemBadge
                );
            }

            const description =
                document.createElement(
                    "p"
                );

            description.textContent =
                workflow.description
                ||
                "No public description yet.";

            identity.append(
                titleRow,
                description
            );

            const stats =
                document.createElement(
                    "div"
                );

            stats.className =
                "admin-workflow-stats";

            const usage =
                document.createElement(
                    "div"
                );

            usage.innerHTML =
                `<span>USED</span><strong>${formatNumber(
                    workflow.usage_count
                    ||
                    0
                )}</strong>`;

            const versions =
                document.createElement(
                    "div"
                );

            versions.innerHTML =
                `<span>VERSION</span><strong>v${workflow.version_number || 1}</strong>`;

            const order =
                document.createElement(
                    "div"
                );

            order.innerHTML =
                `<span>ORDER</span><strong>${workflow.sort_order ?? 100}</strong>`;

            stats.append(
                usage,
                versions,
                order
            );

            const status =
                document.createElement(
                    "span"
                );

            status.className =
                `admin-workflow-status ${
                    workflow.status
                    ||
                    "draft"
                }`;

            status.textContent =
                adminWorkflowStatusLabel(
                    workflow.status
                );

            const actions =
                document.createElement(
                    "div"
                );

            actions.className =
                "admin-workflow-actions";

            const edit =
                document.createElement(
                    "button"
                );

            edit.type =
                "button";

            edit.textContent =
                "Edit";

            edit.addEventListener(
                "click",
                () =>
                    openAdminWorkflowEditor(
                        workflow.id
                    )
            );

            const open =
                document.createElement(
                    "button"
                );

            open.type =
                "button";

            open.textContent =
                "Open in Create";

            open.disabled =
                workflow.status
                !==
                "published";

            open.addEventListener(
                "click",
                async () => {
                    await loadProfiles(
                        workflow.id
                    );

                    showView(
                        "generate"
                    );

                    selectGenerateProfile(
                        workflow.id
                    );

                    window.scrollTo({
                        top: 0,
                        behavior:
                            "smooth",
                    });
                }
            );

            actions.append(
                edit,
                open
            );

            row.append(
                identity,
                stats,
                status,
                actions
            );

            adminWorkflowList.appendChild(
                row
            );
        }
    );
}


function setAdminWorkflowFormMessage(
    message,
    state = ""
) {
    adminWorkflowFormMessage.textContent =
        message;

    adminWorkflowFormMessage.className =
        "connection-result";

    if (state) {
        adminWorkflowFormMessage.classList.add(
            state
        );
    }
}


function selectedAdminWorkflowType() {
    return (
        adminWorkflowTemplateType.checked
            ?
            "template"
            :
            "private"
    );
}


function updateAdminWorkflowSecurityNote() {
    const type =
        selectedAdminWorkflowType();

    if (
        type
        ===
        "template"
    ) {
        adminWorkflowSecurityTitle.textContent =
            "PUBLIC TEMPLATE";

        adminWorkflowSecurityText.textContent =
            (
                "Users can see the instruction and create their own editable copy. "
                +
                "They still cannot change the shared Admin version."
            );
    } else {
        adminWorkflowSecurityTitle.textContent =
            "PRIVATE WORKFLOW";

        adminWorkflowSecurityText.textContent =
            (
                "The instruction is encrypted and never returned through normal user profile APIs."
            );
    }
}


function resetAdminWorkflowForm() {
    editingAdminWorkflowId =
        null;

    editingAdminWorkflowStatus =
        "draft";

    editingAdminWorkflowSystem =
        false;

    adminWorkflowModalTitle.textContent =
        "Add workflow";

    adminWorkflowNameInput.value =
        "";

    adminWorkflowDescriptionInput.value =
        "";

    adminWorkflowSortOrderInput.value =
        "100";

    adminWorkflowInstructionInput.value =
        "";

    adminWorkflowPrivateType.checked =
        true;

    adminWorkflowTemplateType.checked =
        false;

    adminWorkflowPrivateType.disabled =
        false;

    adminWorkflowTemplateType.disabled =
        false;

    adminWorkflowVersionPanel.classList.add(
        "hidden-element"
    );

    adminWorkflowVersionList.innerHTML =
        "";

    duplicateAdminWorkflowButton.classList.add(
        "hidden-element"
    );

    unpublishAdminWorkflowButton.classList.add(
        "hidden-element"
    );

    archiveAdminWorkflowButton.classList.add(
        "hidden-element"
    );

    deleteAdminWorkflowButton.classList.add(
        "hidden-element"
    );

    saveAdminWorkflowDraftButton.textContent =
        "Save draft";

    publishAdminWorkflowButton.textContent =
        "Save & publish";

    setAdminWorkflowFormMessage(
        "Draft workflows are visible only to Admin."
    );

    updateAdminWorkflowSecurityNote();
}


function openNewAdminWorkflowModal() {
    resetAdminWorkflowForm();

    openModal(
        adminWorkflowModal
    );

    requestAnimationFrame(
        () =>
            adminWorkflowNameInput.focus()
    );
}


async function loadAdminWorkflowVersions(
    profileId
) {
    adminWorkflowVersionPanel.classList.remove(
        "hidden-element"
    );

    adminWorkflowVersionList.innerHTML = `
        <div class="loading-state">
            Loading versions…
        </div>
    `;

    try {
        const response =
            await fetch(
                `/api/admin/workflows/${profileId}/versions`,
                {
                    cache:
                        "no-store",
                }
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

        adminWorkflowVersionList.innerHTML =
            "";

        const versions =
            data.versions
            ||
            [];

        if (!versions.length) {
            adminWorkflowVersionList.innerHTML = `
                <div class="loading-state">
                    No previous versions.
                </div>
            `;

            return;
        }

        versions.forEach(
            version => {
                const row =
                    document.createElement(
                        "div"
                    );

                row.className =
                    "admin-workflow-version-row";

                const copy =
                    document.createElement(
                        "div"
                    );

                const title =
                    document.createElement(
                        "strong"
                    );

                title.textContent =
                    `Version ${version.version_number}`;

                const date =
                    document.createElement(
                        "span"
                    );

                date.textContent =
                    version.created_at
                    ||
                    "";

                copy.append(
                    title,
                    date
                );

                const badge =
                    document.createElement(
                        "span"
                    );

                badge.className =
                    "admin-workflow-version-badge";

                badge.textContent =
                    version.is_active
                        ?
                        "CURRENT"
                        :
                        "PREVIOUS";

                const restore =
                    document.createElement(
                        "button"
                    );

                restore.type =
                    "button";

                restore.textContent =
                    "Restore";

                restore.disabled =
                    Boolean(
                        version.is_active
                    );

                restore.addEventListener(
                    "click",
                    async () => {
                        if (
                            !window.confirm(
                                `Restore Version ${version.version_number} as the active workflow instruction?`
                            )
                        ) {
                            return;
                        }

                        restore.disabled =
                            true;

                        try {
                            const response =
                                await fetch(
                                    `/api/admin/workflows/${profileId}/rollback`,
                                    {
                                        method:
                                            "POST",

                                        headers: {
                                            "Content-Type":
                                                "application/json",
                                        },

                                        body:
                                            JSON.stringify({
                                                version_number:
                                                    version.version_number,
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

                            showToast(
                                `Workflow restored to Version ${version.version_number}.`
                            );

                            await openAdminWorkflowEditor(
                                profileId,
                                false
                            );

                            await Promise.all([
                                loadAdminDashboard(),
                                loadProfiles(),
                            ]);

                        } catch (error) {
                            showToast(
                                error.message
                            );

                        } finally {
                            restore.disabled =
                                false;
                        }
                    }
                );

                row.append(
                    copy,
                    badge,
                    restore
                );

                adminWorkflowVersionList.appendChild(
                    row
                );
            }
        );

    } catch (error) {
        adminWorkflowVersionList.innerHTML = `
            <div class="loading-state">
                Could not load versions.
            </div>
        `;

        console.warn(
            "Workflow version loading failed:",
            error
        );
    }
}


async function openAdminWorkflowEditor(
    profileId,
    openTheModal = true
) {
    try {
        const response =
            await fetch(
                `/api/admin/workflows/${profileId}`,
                {
                    cache:
                        "no-store",
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const workflow =
            await response.json();

        editingAdminWorkflowId =
            Number(
                workflow.id
            );

        editingAdminWorkflowStatus =
            workflow.status
            ||
            "draft";

        editingAdminWorkflowSystem =
            Boolean(
                workflow.is_system
            );

        adminWorkflowModalTitle.textContent =
            workflow.name;

        adminWorkflowNameInput.value =
            workflow.name
            ||
            "";

        adminWorkflowDescriptionInput.value =
            workflow.description
            ||
            "";

        adminWorkflowSortOrderInput.value =
            String(
                workflow.sort_order
                ??
                100
            );

        adminWorkflowInstructionInput.value =
            workflow.system_instruction
            ||
            "";

        adminWorkflowPrivateType.checked =
            workflow.workflow_type
            !==
            "template";

        adminWorkflowTemplateType.checked =
            workflow.workflow_type
            ===
            "template";

        // Keep version history unambiguous: workflow type is chosen once.
        // To create the other type, duplicate and choose the type on the new draft.
        adminWorkflowPrivateType.disabled =
            true;

        adminWorkflowTemplateType.disabled =
            true;

        duplicateAdminWorkflowButton.classList.remove(
            "hidden-element"
        );

        unpublishAdminWorkflowButton.classList.toggle(
            "hidden-element",
            workflow.status
            !==
            "published"
        );

        archiveAdminWorkflowButton.classList.remove(
            "hidden-element"
        );

        archiveAdminWorkflowButton.textContent =
            workflow.status
            ===
            "archived"
                ?
                "Restore to draft"
                :
                "Archive";

        deleteAdminWorkflowButton.classList.toggle(
            "hidden-element",
            Boolean(
                workflow.is_system
            )
        );

        saveAdminWorkflowDraftButton.textContent =
            workflow.status
            ===
            "published"
                ?
                "Save changes"
                :
                "Save";

        publishAdminWorkflowButton.textContent =
            workflow.status
            ===
            "published"
                ?
                "Save & keep published"
                :
                "Save & publish";

        setAdminWorkflowFormMessage(
            `${adminWorkflowTypeLabel(workflow)} · ${adminWorkflowStatusLabel(workflow.status)} · Used ${formatNumber(workflow.usage_count || 0)} times`
        );

        updateAdminWorkflowSecurityNote();

        await loadAdminWorkflowVersions(
            workflow.id
        );

        if (openTheModal) {
            openModal(
                adminWorkflowModal
            );
        }

    } catch (error) {
        showToast(
            error.message
        );
    }
}


function adminWorkflowPayload() {
    const name =
        adminWorkflowNameInput
            .value
            .trim();

    const description =
        adminWorkflowDescriptionInput
            .value
            .trim();

    const instruction =
        adminWorkflowInstructionInput
            .value
            .trim();

    const sortOrder =
        Math.max(
            0,
            Number(
                adminWorkflowSortOrderInput
                    .value
                ||
                100
            )
        );

    if (!name) {
        throw new Error(
            "Enter a workflow name."
        );
    }

    if (!instruction) {
        throw new Error(
            "Enter a system instruction."
        );
    }

    return {
        name:
            name,
        description:
            description,
        system_instruction:
            instruction,
        workflow_type:
            selectedAdminWorkflowType(),
        sort_order:
            sortOrder,
    };
}


async function saveAdminWorkflow(
    publish = false
) {
    const payload =
        adminWorkflowPayload();

    saveAdminWorkflowDraftButton.disabled =
        true;

    publishAdminWorkflowButton.disabled =
        true;

    try {
        let workflow;

        if (
            editingAdminWorkflowId
        ) {
            const response =
                await fetch(
                    `/api/admin/workflows/${editingAdminWorkflowId}`,
                    {
                        method:
                            "PATCH",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body:
                            JSON.stringify(
                                payload
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

            workflow =
                await response.json();

        } else {
            const response =
                await fetch(
                    "/api/admin/workflows",
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body:
                            JSON.stringify({
                                ...payload,
                                status:
                                    publish
                                        ?
                                        "published"
                                        :
                                        "draft",
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

            workflow =
                await response.json();

            editingAdminWorkflowId =
                Number(
                    workflow.id
                );
        }

        if (
            publish
            &&
            workflow.status
            !==
            "published"
        ) {
            const statusResponse =
                await fetch(
                    `/api/admin/workflows/${workflow.id}/status`,
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body:
                            JSON.stringify({
                                status:
                                    "published",
                            }),
                    }
                );

            if (!statusResponse.ok) {
                throw new Error(
                    await apiError(
                        statusResponse
                    )
                );
            }

            workflow =
                await statusResponse.json();
        }

        showToast(
            publish
                ?
                "Workflow published to all users."
                :
                "Workflow saved."
        );

        await Promise.all([
            loadAdminDashboard(),
            loadProfiles(),
            loadManagerProfiles(),
        ]);

        await openAdminWorkflowEditor(
            workflow.id,
            false
        );

        if (
            !publish
            &&
            !editingAdminWorkflowId
        ) {
            closeModal(
                adminWorkflowModal
            );
        }

    } catch (error) {
        setAdminWorkflowFormMessage(
            error.message,
            "error"
        );

    } finally {
        saveAdminWorkflowDraftButton.disabled =
            false;

        publishAdminWorkflowButton.disabled =
            false;
    }
}


async function setAdminWorkflowStatus(
    status
) {
    if (!editingAdminWorkflowId) {
        return;
    }

    try {
        const response =
            await fetch(
                `/api/admin/workflows/${editingAdminWorkflowId}/status`,
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify({
                            status:
                                status,
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

        showToast(
            status
            ===
            "published"
                ?
                "Workflow published."
                :
                status
                ===
                "archived"
                    ?
                    "Workflow archived."
                    :
                    "Workflow unpublished."
        );

        await Promise.all([
            loadAdminDashboard(),
            loadProfiles(),
            loadManagerProfiles(),
        ]);

        await openAdminWorkflowEditor(
            editingAdminWorkflowId,
            false
        );

    } catch (error) {
        showToast(
            error.message
        );
    }
}


addAdminWorkflowButton.addEventListener(
    "click",
    openNewAdminWorkflowModal
);


adminWorkflowPrivateType.addEventListener(
    "change",
    updateAdminWorkflowSecurityNote
);


adminWorkflowTemplateType.addEventListener(
    "change",
    updateAdminWorkflowSecurityNote
);


saveAdminWorkflowDraftButton.addEventListener(
    "click",
    () =>
        saveAdminWorkflow(
            false
        )
);


publishAdminWorkflowButton.addEventListener(
    "click",
    () =>
        saveAdminWorkflow(
            true
        )
);


unpublishAdminWorkflowButton.addEventListener(
    "click",
    async () => {
        if (
            window.confirm(
                "Unpublish this workflow? It will disappear from new user generations but old jobs remain unchanged."
            )
        ) {
            await setAdminWorkflowStatus(
                "unpublished"
            );
        }
    }
);


archiveAdminWorkflowButton.addEventListener(
    "click",
    async () => {
        if (!editingAdminWorkflowId) {
            return;
        }

        if (
            editingAdminWorkflowStatus
            ===
            "archived"
        ) {
            await setAdminWorkflowStatus(
                "draft"
            );

            return;
        }

        if (
            window.confirm(
                "Archive this workflow? It will be hidden from users and kept for history."
            )
        ) {
            await setAdminWorkflowStatus(
                "archived"
            );
        }
    }
);


duplicateAdminWorkflowButton.addEventListener(
    "click",
    async () => {
        if (!editingAdminWorkflowId) {
            return;
        }

        duplicateAdminWorkflowButton.disabled =
            true;

        try {
            const response =
                await fetch(
                    `/api/admin/workflows/${editingAdminWorkflowId}/duplicate`,
                    {
                        method:
                            "POST",
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(
                        response
                    )
                );
            }

            const workflow =
                await response.json();

            showToast(
                "Draft copy created."
            );

            await loadAdminDashboard();

            await openAdminWorkflowEditor(
                workflow.id,
                false
            );

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            duplicateAdminWorkflowButton.disabled =
                false;
        }
    }
);


deleteAdminWorkflowButton.addEventListener(
    "click",
    async () => {
        if (!editingAdminWorkflowId) {
            return;
        }

        if (
            !window.confirm(
                "Delete this workflow permanently? This is allowed only when it has no generation history."
            )
        ) {
            return;
        }

        deleteAdminWorkflowButton.disabled =
            true;

        try {
            const response =
                await fetch(
                    `/api/admin/workflows/${editingAdminWorkflowId}`,
                    {
                        method:
                            "DELETE",
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
                adminWorkflowModal
            );

            showToast(
                "Workflow deleted."
            );

            await Promise.all([
                loadAdminDashboard(),
                loadProfiles(),
                loadManagerProfiles(),
            ]);

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            deleteAdminWorkflowButton.disabled =
                false;
        }
    }
);


function renderAdminSystem(system) {
    adminSystemList.innerHTML = "";

    [
        ["Authentication", system.auth],
        ["Database", system.database],
        ["Image storage", system.storage],
        ["Background jobs", system.queue],
    ].forEach(([title, item]) => {
        item = item || {};

        const row = document.createElement("article");
        row.className = "admin-system-row";

        const copy = document.createElement("div");
        const heading = document.createElement("strong");
        const detail = document.createElement("span");
        heading.textContent = title;
        detail.textContent = item.label || item.provider || "Not configured";
        copy.append(heading, detail);

        const status = document.createElement("span");
        status.className = `admin-connection-status ${item.configured ? "connected" : "missing"}`;
        status.textContent = item.configured ? "Connected" : "Needs setup";

        row.append(copy, status);
        adminSystemList.appendChild(row);
    });
}


function tierLabel(tier) {
    if (tier === "premium") return "Best Quality";
    if (tier === "balanced") return "Balanced";
    return "Economy";
}


function renderAdminModels(models) {
    adminModelList.innerHTML = "";

    if (!models.length) {
        adminModelList.innerHTML = `<div class="loading-state">No AI models configured.</div>`;
        return;
    }

    models.forEach(model => {
        const row = document.createElement("article");
        row.className = "admin-model-row simple";

        const meta = document.createElement("div");
        meta.className = "admin-row-meta";
        const heading = document.createElement("strong");
        const tier = document.createElement("span");
        heading.textContent = `${capitalize(model.provider)} · ${model.capability === "planner" ? "Prompt Planner" : "Image Generator"}`;
        tier.textContent = tierLabel(model.tier);
        meta.append(heading, tier);

        const modelInput = document.createElement("input");
        modelInput.type = "text";
        modelInput.value = model.model_id || "";
        modelInput.placeholder = "Provider model ID";

        const enabledLabel = document.createElement("label");
        enabledLabel.className = "admin-inline-check";
        const enabled = document.createElement("input");
        enabled.type = "checkbox";
        enabled.checked = Boolean(model.enabled);
        const enabledText = document.createElement("span");
        enabledText.textContent = "Available";
        enabledLabel.append(enabled, enabledText);

        const save = document.createElement("button");
        save.type = "button";
        save.textContent = "Save";
        save.onclick = async () => {
            save.disabled = true;
            try {
                const response = await fetch(`/api/admin/models/${model.id}`, {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        model_id: modelInput.value.trim(),
                        enabled: enabled.checked,
                    }),
                });
                if (!response.ok) throw new Error(await apiError(response));
                await response.json();
                showToast(`${tierLabel(model.tier)} model saved.`);
                await Promise.all([loadAdminDashboard(), loadSettings()]);
            } catch (error) {
                showToast(error.message);
            } finally {
                save.disabled = false;
            }
        };

        row.append(meta, modelInput, enabledLabel, save);
        adminModelList.appendChild(row);
    });
}


function renderAdminUsers(users) {
    adminUserList.innerHTML = "";

    if (!users.length) {
        adminUserList.innerHTML = `<div class="loading-state">No users yet.</div>`;
        return;
    }

    users.forEach(user => {
        const row = document.createElement("article");
        row.className = "admin-user-row simple";

        const copy = document.createElement("div");
        copy.className = "admin-user-copy";
        const email = document.createElement("strong");
        const meta = document.createElement("span");
        email.textContent = user.email || user.user_id;
        meta.textContent = `${formatNumber(user.job_count || 0)} jobs · ${formatNumber(user.image_count || 0)} images`;
        copy.append(email, meta);

        const role = document.createElement("select");
        ["user", "support", "admin"].forEach(value => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value === "admin" ? "Admin" : value === "support" ? "Support" : "User";
            option.selected = user.role === value;
            role.appendChild(option);
        });

        const status = document.createElement("select");
        ["active", "suspended"].forEach(value => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value === "active" ? "Active" : "Suspended";
            option.selected = user.status === value;
            status.appendChild(option);
        });

        const save = document.createElement("button");
        save.type = "button";
        save.textContent = "Save";
        save.onclick = async () => {
            save.disabled = true;
            try {
                const response = await fetch(`/api/admin/users/${encodeURIComponent(user.user_id)}`, {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ role: role.value, status: status.value }),
                });
                if (!response.ok) throw new Error(await apiError(response));
                await response.json();
                showToast("User updated.");
                await loadAdminDashboard();
            } catch (error) {
                showToast(error.message);
            } finally {
                save.disabled = false;
            }
        };

        row.append(copy, role, status, save);
        adminUserList.appendChild(row);
    });
}


function renderAdminFailures(failures) {
    adminFailureList.innerHTML = "";

    if (!failures.length) {
        adminFailureList.innerHTML = `
            <div class="admin-empty-success">
                <strong>No recent generation errors.</strong>
                <span>Everything looks healthy.</span>
            </div>
        `;
        return;
    }

    failures.forEach(item => {
        const row = document.createElement("article");
        row.className = "admin-failure-row";

        const title = document.createElement("strong");
        title.textContent = `Job #${item.job_id} · ${item.user_email || "Unknown user"}`;

        const meta = document.createElement("span");
        meta.textContent = `${providerLabel(item.provider || "")} · ${item.model || "model unavailable"}`;

        const error = document.createElement("p");
        error.textContent = friendlyError(item.error_message || "Generation failed.");

        row.append(title, meta, error);
        adminFailureList.appendChild(row);
    });
}


refreshAdminButton.addEventListener(
    "click",
    loadAdminDashboard
);


/* =========================================================
   VIEW NAVIGATION
========================================================= */

function showView(
    view
) {
    document.body.dataset.hyperexView =
        view;

    const mapping = {
        generate:
            generateView,
        profiles:
            profilesView,
        history:
            historyView,
        settings:
            settingsView,
        admin:
            adminView,
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

    navAdmin.classList.toggle(
        "active",
        view === "admin"
    );

    const mobileMap = {
        generate:
            mobileNavCreate,
        profiles:
            mobileNavProfiles,
        history:
            mobileNavHistory,
        settings:
            mobileNavSettings,
        admin:
            mobileNavAdmin,
    };

    Object.entries(
        mobileMap
    ).forEach(
        ([name, element]) => {
            if (!element) {
                return;
            }

            element.classList.toggle(
                "active",
                name === view
            );
        }
    );

    if (mobileGenerateDock) {
        mobileGenerateDock.classList.toggle(
            "hidden-element",
            view !== "generate"
        );
    }
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


navAdmin.addEventListener(
    "click",
    async () => {
        if (
            currentUser?.role
            !==
            "admin"
        ) {
            showToast(
                "Administrator access required."
            );

            return;
        }

        showView(
            "admin"
        );

        await loadAdminDashboard();
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


if (mobileNavCreate) {
    mobileNavCreate.addEventListener(
        "click",
        () => navGenerate.click()
    );

    mobileNavProfiles.addEventListener(
        "click",
        () => navProfiles.click()
    );

    mobileNavHistory.addEventListener(
        "click",
        () => navHistory.click()
    );

    mobileNavSettings.addEventListener(
        "click",
        () => navSettings.click()
    );

    if (mobileNavAdmin) {
        mobileNavAdmin.addEventListener(
            "click",
            () => navAdmin.click()
        );
    }
}

if (mobileGenerateButton) {
    mobileGenerateButton.addEventListener(
        "click",
        () => generateButton.click()
    );
}


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
            "Check the connected provider key in Settings."
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
                "/api/settings",
                {
                    cache: "no-store",
                }
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

        // Render the page immediately. Provider-key suffix details are a
        // secondary request and must never block model choices / Create.
        renderSettings();
        renderCreateProviderSummary();
        seedProviderConnectionsFromSettings();

        loadProviderConnections()
            .catch(
                error =>
                    console.warn(
                        "Provider connection refresh failed:",
                        error
                    )
            );

    } catch (error) {
        console.error(
            error
        );

        plannerProviderStatus.textContent =
            "LOAD ERROR";

        imageProviderStatus.textContent =
            "LOAD ERROR";

        plannerConnectionSummary.textContent =
            "Settings could not load. Refresh Hyperex and try again.";

        imageConnectionSummary.textContent =
            "Settings could not load. Refresh Hyperex and try again.";

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

    fillSelect(
        confirmBatchOverSelect,
        catalog.confirm_batch_over,
        settings.confirm_batch_over
    );

    fillSelect(
        maxOutputCountSelect,
        catalog.max_output_count,
        settings.max_output_count
    );

    autoGenerateImages.checked =
        Boolean(
            settings.auto_generate_images
        );

    draftAutosaveCheckbox.checked =
        Boolean(
            settings.draft_autosave
        );

    renderConnectionBadges();
    renderPlannerSettingsState();
    renderImageSettingsState();
}


function renderTierSelect(
    element,
    items,
    selectedTier
) {
    element.innerHTML = "";

    const available = items.some(
        item =>
            item.id
            ===
            selectedTier
    );

    if (
        selectedTier
        &&
        !available
    ) {
        const unavailable =
            document.createElement(
                "option"
            );

        unavailable.value =
            selectedTier;

        unavailable.textContent =
            `${tierDisplayName(selectedTier)} — unavailable`;

        unavailable.disabled =
            true;

        unavailable.selected =
            true;

        element.appendChild(
            unavailable
        );
    }

    items.forEach(
        item => {
            const option =
                document.createElement(
                    "option"
                );

            option.value =
                item.id;

            option.textContent =
                item.label;

            option.selected =
                item.id
                ===
                selectedTier;

            element.appendChild(
                option
            );
        }
    );
}


function tierBenefit(
    tier
) {
    if (tier === "premium") {
        return "Strongest results";
    }

    if (tier === "balanced") {
        return "Recommended";
    }

    return "Lowest usage";
}


function syncTierChoiceSelection(
    container,
    selectedTier
) {
    if (!container) {
        return;
    }

    container
        .querySelectorAll(
            ".tier-choice"
        )
        .forEach(
            button => {
                button.classList.toggle(
                    "selected",
                    button.dataset.tier
                    ===
                    selectedTier
                );

                button.setAttribute(
                    "aria-pressed",
                    button.dataset.tier
                    ===
                    selectedTier
                        ?
                        "true"
                        :
                        "false"
                );
            }
        );
}


function renderTierChoices(
    container,
    selectElement,
    items,
    selectedTier
) {
    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (!items.length) {
        const empty =
            document.createElement(
                "div"
            );

        empty.className =
            "tier-unavailable-note";

        empty.textContent =
            "No quality levels are enabled for this provider.";

        container.appendChild(
            empty
        );

        return;
    }

    const selectedAvailable =
        items.some(
            item =>
                item.id
                ===
                selectedTier
        );

    if (
        selectedTier
        &&
        !selectedAvailable
    ) {
        const warning =
            document.createElement(
                "div"
            );

        warning.className =
            "tier-unavailable-note";

        warning.textContent =
            `${tierDisplayName(selectedTier)} is currently disabled. Choose another level.`;

        container.appendChild(
            warning
        );
    }

    items.forEach(
        item => {
            const button =
                document.createElement(
                    "button"
                );

            button.type =
                "button";

            button.dataset.tier =
                item.id;

            button.className =
                `tier-choice tier-choice-${item.id}`;

            const title =
                document.createElement(
                    "strong"
                );

            title.textContent =
                item.label;

            const benefit =
                document.createElement(
                    "span"
                );

            benefit.textContent =
                tierBenefit(
                    item.id
                );

            const model =
                document.createElement(
                    "small"
                );

            model.textContent =
                item.model_id;

            button.append(
                title,
                benefit,
                model
            );

            button.addEventListener(
                "click",
                () => {
                    selectElement.value =
                        item.id;

                    syncTierChoiceSelection(
                        container,
                        item.id
                    );

                    selectElement.dispatchEvent(
                        new Event(
                            "change"
                        )
                    );
                }
            );

            container.appendChild(
                button
            );
        }
    );

    syncTierChoiceSelection(
        container,
        selectedTier
    );
}


function currentTierItem(
    capability,
    provider,
    tier
) {
    const catalog =
        capability
        ===
        "planner"
            ?
            settingsPayload
                ?.catalog
                ?.planner_tiers
            :
            settingsPayload
                ?.catalog
                ?.image_tiers;

    return (
        catalog
        ?.[provider]
        ?.find(
            item =>
                item.id
                ===
                tier
        )
        ||
        null
    );
}


function renderPlannerTierDetail() {
    if (!settingsPayload) {
        return;
    }

    const provider =
        plannerProviderSelect.value
        ||
        settingsPayload.settings
            .planner_provider;

    const tier =
        plannerModelSelect.value
        ||
        settingsPayload.settings
            .planner_tier;

    const item =
        currentTierItem(
            "planner",
            provider,
            tier
        );

    if (!item) {
        plannerResolvedModel.textContent =
            "Choose another level";

        plannerTierNote.textContent =
            "This quality level is not currently available.";

        return;
    }

    plannerResolvedModel.textContent =
        item.model_id;

    plannerTierNote.textContent =
        item.note
        ||
        "Hyperex will use this model for new jobs.";
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

    const items =
        settingsPayload.catalog
            .planner_tiers[
                provider
            ]
        ||
        [];

    const currentValue =
        plannerModelSelect.value;

    const selected =
        currentValue
        ||
        settingsPayload.settings
            .planner_tier;

    renderTierSelect(
        plannerModelSelect,
        items,
        selected
    );

    renderTierChoices(
        plannerTierChoices,
        plannerModelSelect,
        items,
        plannerModelSelect.value
        ||
        selected
    );

    openaiReasoningField.classList.add(
        "hidden-element"
    );

    renderPlannerTierDetail();
}


function renderImageTierDetail() {
    if (!settingsPayload) {
        return;
    }

    const provider =
        imageProviderSelect.value
        ||
        settingsPayload.settings
            .image_provider;

    const tier =
        imageModelSelect.value
        ||
        settingsPayload.settings
            .image_tier;

    const item =
        currentTierItem(
            "image",
            provider,
            tier
        );

    if (!item) {
        imageResolvedModel.textContent =
            "Choose another level";

        imageTierNote.textContent =
            "This quality level is not currently available.";

        return;
    }

    imageResolvedModel.textContent =
        item.model_id;

    imageTierNote.textContent =
        item.note
        ||
        "Hyperex will use this model for new jobs.";
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

    const items =
        settingsPayload.catalog
            .image_tiers[
                provider
            ]
        ||
        [];

    const currentValue =
        imageModelSelect.value;

    const selected =
        currentValue
        ||
        settingsPayload.settings
            .image_tier;

    renderTierSelect(
        imageModelSelect,
        items,
        selected
    );

    renderTierChoices(
        imageTierChoices,
        imageModelSelect,
        items,
        imageModelSelect.value
        ||
        selected
    );

    openaiQualityField.classList.add(
        "hidden-element"
    );

    geminiAspectField.classList.add(
        "hidden-element"
    );

    renderImageTierDetail();
}


function seedProviderConnectionsFromSettings() {
    if (!settingsPayload) {
        return;
    }

    const planner =
        settingsPayload.planner
        ||
        {};

    const image =
        settingsPayload.image
        ||
        {};

    const statusFor =
        provider => {
            const plannerItem =
                planner
                    ?.providers
                    ?.[provider]
                ||
                {};

            const imageItem =
                image
                    ?.providers
                    ?.[provider]
                ||
                {};

            return {
                saved: false,
                configured:
                    Boolean(
                        plannerItem.configured
                        ||
                        imageItem.configured
                    ),
                source:
                    plannerItem.key_source
                    ||
                    imageItem.key_source
                    ||
                    null,
            };
        };

    providerConnections = {
        openai:
            statusFor(
                "openai"
            ),
        gemini:
            statusFor(
                "gemini"
            ),
    };

    renderProviderConnections();
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

    const tier =
        plannerModelSelect.value;

    const tierAvailable =
        Boolean(
            currentTierItem(
                "planner",
                provider,
                tier
            )
        );

    const providerStatus =
        settingsPayload
            ?.planner
            ?.providers
            ?.[provider];

    const configured =
        Boolean(
            providerStatus
                ?.configured
        );

    plannerProviderStatus.textContent =
        !tierAvailable
            ?
            "CHOOSE LEVEL"
            :
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
            &&
            tierAvailable
        );

    plannerProviderStatus
        .classList
        .toggle(
            "warning",
            !configured
            ||
            !tierAvailable
        );

    plannerConnectionSummary.textContent =
        !tierAvailable
            ?
            "This quality level is disabled. Choose another level."
            :
            configured
                ?
                `${provider.toUpperCase()} is connected and ready.`
                :
                `${provider.toUpperCase()} is not connected. Add its API key above.`;
}


function renderImageSettingsState() {
    const provider =
        imageProviderSelect.value;

    const tier =
        imageModelSelect.value;

    const tierAvailable =
        Boolean(
            currentTierItem(
                "image",
                provider,
                tier
            )
        );

    const providerStatus =
        settingsPayload
            ?.image
            ?.providers
            ?.[provider];

    const configured =
        Boolean(
            providerStatus
                ?.configured
        );

    imageProviderStatus.textContent =
        !tierAvailable
            ?
            "CHOOSE LEVEL"
            :
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
            &&
            tierAvailable
        );

    imageProviderStatus
        .classList
        .toggle(
            "warning",
            !configured
            ||
            !tierAvailable
        );

    imageConnectionSummary.textContent =
        !tierAvailable
            ?
            "This quality level is disabled. Choose another level."
            :
            configured
                ?
                `${provider.toUpperCase()} is connected and ready.`
                :
                `${provider.toUpperCase()} is not connected. Add its API key above.`;
}


plannerProviderSelect.addEventListener(
    "change",
    () => {
        renderPlannerModelOptions();
        renderPlannerSettingsState();
    }
);


plannerModelSelect.addEventListener(
    "change",
    () => {
        renderPlannerTierDetail();
        renderPlannerSettingsState();
        updateCreateCostEstimate();
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
        renderImageTierDetail();
        renderImageSettingsState();
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

        planner_tier:
            plannerModelSelect.value,

        image_provider:
            providerImage,

        image_tier:
            imageModelSelect.value,

        batch_concurrency:
            Number(
                batchConcurrencySelect
                    .value
            ),

        auto_generate_images:
            autoGenerateImages.checked,

        confirm_batch_over:
            Number(
                confirmBatchOverSelect
                    .value
            ),

        max_output_count:
            Number(
                maxOutputCountSelect
                    .value
            ),

        draft_autosave:
            draftAutosaveCheckbox.checked,
    };

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

        await response.json();

        await loadSettings();

        showToast(
            "Hyperex quality settings saved."
        );

    } catch (error) {
        console.error(
            error
        );

        showToast(
            error.message
        );

        throw error;

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
   PROVIDER CONNECTIONS
========================================================= */

async function loadProviderConnections(
    force = false
) {
    const cacheAge =
        Date.now()
        -
        providerConnectionsLoadedAt;

    if (
        !force
        &&
        providerConnections
        &&
        providerConnectionsLoadedAt
        &&
        cacheAge < 10000
    ) {
        renderProviderConnections();
        return providerConnections;
    }

    const controller =
        new AbortController();

    const timeout =
        window.setTimeout(
            () =>
                controller.abort(),
            5000
        );

    try {
        const response =
            await fetch(
                "/api/provider-connections",
                {
                    cache: "no-store",
                    signal:
                        controller.signal,
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        providerConnections =
            await response.json();

        providerConnectionsLoadedAt =
            Date.now();

        renderProviderConnections();

        return providerConnections;

    } catch (error) {
        // The Settings page already has a fast status snapshot from
        // /api/settings. A slow secondary key-suffix refresh must not leave
        // the entire page stuck on "Checking…".
        if (!providerConnections) {
            openaiKeyConnectionText.textContent =
                "Status unavailable";

            geminiKeyConnectionText.textContent =
                "Status unavailable";
        }

        if (
            error.name
            !==
            "AbortError"
        ) {
            console.warn(
                "Provider connection refresh failed:",
                error
            );
        }

        return providerConnections;

    } finally {
        window.clearTimeout(
            timeout
        );
    }
}


function renderProviderConnections() {
    if (!providerConnections) {
        return;
    }

    renderProviderConnectionLine(
        "openai",
        openaiKeyConnectionText,
        removeOpenaiKeyButton
    );

    renderProviderConnectionLine(
        "gemini",
        geminiKeyConnectionText,
        removeGeminiKeyButton
    );
}


function renderProviderConnectionLine(
    provider,
    textElement,
    removeButton
) {
    const item =
        providerConnections[
            provider
        ]
        ||
        {};

    if (item.saved) {
        textElement.textContent =
            `Saved ·••••${item.key_suffix || ""}`;

        removeButton.disabled =
            false;

        return;
    }

    if (item.configured) {
        textElement.textContent =
            item.source
            ===
            "saved_connection"
                ?
                "Connected"
                :
                "Using server fallback key";

        removeButton.disabled =
            true;

        return;
    }

    textElement.textContent =
        "Not connected";

    removeButton.disabled =
        true;
}


async function saveProviderKey(
    provider,
    input,
    button
) {
    const apiKey =
        input
        .value
        .trim();

    if (!apiKey) {
        showToast(
            `Paste a ${provider} API key first.`
        );

        return;
    }

    button.disabled =
        true;

    const original =
        button.textContent;

    button.textContent =
        "Testing…";

    providerKeyResult.className =
        "connection-result";

    providerKeyResult.textContent =
        `Testing ${provider.toUpperCase()}…`;

    try {
        const response =
            await fetch(
                `/api/provider-connections/${provider}`,
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify({
                            api_key:
                                apiKey,
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

        input.value =
            "";

        providerKeyResult.className =
            "connection-result success";

        providerKeyResult.textContent =
            `${provider.toUpperCase()} connected and encrypted.`;

        providerConnectionsLoadedAt = 0;
        await loadSettings();

    } catch (error) {
        providerKeyResult.className =
            "connection-result error";

        providerKeyResult.textContent =
            error.message;

    } finally {
        button.disabled =
            false;

        button.textContent =
            original;
    }
}


async function removeProviderKey(
    provider
) {
    const confirmed =
        window.confirm(
            `Disconnect the saved ${provider.toUpperCase()} key?`
        );

    if (!confirmed) {
        return;
    }

    try {
        const response =
            await fetch(
                `/api/provider-connections/${provider}`,
                {
                    method:
                        "DELETE",
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

        providerKeyResult.className =
            "connection-result success";

        providerKeyResult.textContent =
            `${provider.toUpperCase()} saved key disconnected.`;

        providerConnectionsLoadedAt = 0;
        await loadSettings();

    } catch (error) {
        providerKeyResult.className =
            "connection-result error";

        providerKeyResult.textContent =
            error.message;
    }
}


saveOpenaiKeyButton.addEventListener(
    "click",
    () =>
        saveProviderKey(
            "openai",
            openaiApiKeyInput,
            saveOpenaiKeyButton
        )
);


saveGeminiKeyButton.addEventListener(
    "click",
    () =>
        saveProviderKey(
            "gemini",
            geminiApiKeyInput,
            saveGeminiKeyButton
        )
);


removeOpenaiKeyButton.addEventListener(
    "click",
    () =>
        removeProviderKey(
            "openai"
        )
);


removeGeminiKeyButton.addEventListener(
    "click",
    () =>
        removeProviderKey(
            "gemini"
        )
);


/* =========================================================
   CREATE PROVIDER SUMMARY / COST
========================================================= */

function tierDisplayName(
    tier
) {
    if (tier === "premium") {
        return "Best Quality";
    }

    return capitalize(
        tier
        ||
        "economy"
    );
}


function renderCreateProviderSummary() {
    if (!settingsPayload) {
        return;
    }

    const settings =
        settingsPayload.settings;

    const plannerProvider =
        settings.planner_provider;

    const plannerName =
        plannerProvider
        ===
        "gemini"
            ?
            "Gemini"
            :
            "OpenAI";

    createPlannerSummary.textContent =
        `${plannerName} · ${tierDisplayName(settings.planner_tier)}`;

    const imageProvider =
        settings.image_provider;

    const imageName =
        imageProvider
        ===
        "gemini"
            ?
            "Gemini"
            :
            "OpenAI";

    createImageSummary.textContent =
        `${imageName} · ${tierDisplayName(settings.image_tier)}`;

    summaryPlanner.textContent =
        `${plannerName} · ${tierDisplayName(settings.planner_tier)} · ${settings.planner_resolved_model || "Unavailable"}`;

    summaryImageEngine.textContent =
        `${imageName} · ${tierDisplayName(settings.image_tier)} · ${settings.image_resolved_model || "Unavailable"}`;

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
        selectedCount
        ===
        "auto"
            ?
            "Auto"
            :
            selectedCount;

    createCostEstimate.textContent =
        `${count} outputs · ${tierDisplayName(settings.image_tier)} · provider billed`;
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
        selected.id,
        false
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

    if (
        profile.workflow_type
        ===
        "private"
    ) {
        card.classList.add(
            "private-workflow"
        );
    }

    if (
        profile.workflow_type
        ===
        "template"
    ) {
        card.classList.add(
            "template-workflow"
        );
    }

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

    const privateBadge =
        document.createElement(
            "span"
        );

    if (
        isManagedProfile(
            profile
        )
    ) {
        privateBadge.className =
            (
                profile.workflow_type
                ===
                "template"
                    ?
                    "profile-private-badge template"
                    :
                    "profile-private-badge"
            );

        privateBadge.textContent =
            profile.workflow_type
            ===
            "template"
                ?
                "HYPEREX · PUBLIC TEMPLATE"
                :
                "HYPEREX · PRIVATE";
    }

    const check =
        document.createElement(
            "span"
        );

    check.className =
        "profile-check";

    check.textContent =
        "●";

    text.append(
        title
    );

    if (
        isManagedProfile(
            profile
        )
    ) {
        text.append(
            privateBadge
        );
    }

    text.append(
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
    profileId,
    saveDraft = true
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
        isManagedProfile(
            profile
        )
            ?
            (
                profile.workflow_type
                ===
                "template"
                    ?
                    `template · v${profile.active_version_number || 1}`
                    :
                    "private"
            )
            :
            (
                profile.active_version_number
                    ?
                    `v${profile.active_version_number}`
                    :
                    "current"
            );

    if (saveDraft) {
        saveCreateDraft();
    }
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


const COMMON_IMAGE_EXTENSIONS = new Set([
    "jpg", "jpeg", "png", "webp", "gif", "bmp",
    "tif", "tiff", "heic", "heif", "avif", "jp2", "j2k",
    "psd", "tga", "dds", "pcx", "ppm", "pgm", "pbm",
    "ico", "qoi"
]);


function looksLikeImageFile(
    file
) {
    if (
        file?.type
        &&
        file.type.startsWith(
            "image/"
        )
    ) {
        return true;
    }

    const name =
        String(
            file?.name
            ||
            ""
        );

    const extension =
        name.includes(".")
            ? name.split(".").pop().toLowerCase()
            : "";

    return COMMON_IMAGE_EXTENSIONS.has(
        extension
    );
}


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
                !looksLikeImageFile(
                    file
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
    const incomingFiles =
        Array.from(
            files
        );

    const imageFiles =
        incomingFiles.filter(
            file =>
                looksLikeImageFile(
                    file
                )
        );

    if (
        imageFiles.length
        !==
        incomingFiles.length
    ) {
        showToast(
            "Some non-image files were skipped."
        );
    }

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

            const previewFallback =
                document.createElement(
                    "div"
                );

            previewFallback.className =
                "reference-preview-fallback hidden-element";

            const previewLabel =
                document.createElement(
                    "strong"
                );

            previewLabel.textContent =
                `IMAGE ${index + 1}`;

            const previewFilename =
                document.createElement(
                    "span"
                );

            previewFilename.textContent =
                file.name
                ||
                "Reference image";

            previewFallback.append(
                previewLabel,
                previewFilename
            );

            image.src =
                url;

            image.alt =
                `Reference ${index + 1}`;

            image.onload =
                () => {
                    URL.revokeObjectURL(
                        url
                    );
                };

            image.onerror =
                () => {
                    URL.revokeObjectURL(
                        url
                    );

                    image.classList.add(
                        "hidden-element"
                    );

                    previewFallback.classList.remove(
                        "hidden-element"
                    );
                };

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
                previewFallback,
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

        saveCreateDraft();
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
                    saveCreateDraft();
                }
            );
        }
    );



autoGenerateImages.addEventListener(
    "change",
    saveCreateDraft
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

    const runtime =
        settingsPayload?.settings;

    if (!runtime) {
        showToast(
            "Settings are still loading. Try again in a moment."
        );

        return;
    }

    if (!runtime.planner_tier_available) {
        showToast(
            "Your prompt quality level is unavailable. Choose another level in Settings."
        );

        showView(
            "settings"
        );

        return;
    }

    const plannerReady =
        Boolean(
            settingsPayload
                ?.planner
                ?.providers
                ?.[runtime.planner_provider]
                ?.configured
        );

    if (!plannerReady) {
        showToast(
            `Connect ${runtime.planner_provider === "openai" ? "OpenAI" : "Gemini"} in Settings before generating.`
        );

        showView(
            "settings"
        );

        return;
    }

    if (
        autoGenerateImages.checked
        &&
        !runtime.image_tier_available
    ) {
        showToast(
            "Your image quality level is unavailable. Choose another level in Settings."
        );

        showView(
            "settings"
        );

        return;
    }

    const imageReady =
        Boolean(
            settingsPayload
                ?.image
                ?.providers
                ?.[runtime.image_provider]
                ?.configured
        );

    if (
        autoGenerateImages.checked
        &&
        !imageReady
    ) {
        showToast(
            `Connect ${runtime.image_provider === "openai" ? "OpenAI" : "Gemini"} in Settings before generating images.`
        );

        showView(
            "settings"
        );

        return;
    }

    if (
        !confirmGenerationSafety()
    ) {
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

    formData.append(
        "aspect_ratio",
        selectedAspectRatio
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

    if (mobileGenerateButton) {
        mobileGenerateButton.disabled =
            busy;

        mobileGenerateButton.innerHTML =
            busy
                ?
                `${label}<span>…</span>`
                :
                `GENERATE<span>→</span>`;
    }
}


function renderPreparedJob(
    job
) {
    if (newGenerationButton) {
        newGenerationButton.classList.add(
            "hidden-element"
        );

        newGenerationButton.disabled =
            true;
    }
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

    summaryRatio.textContent =
        job.aspect_ratio
        ||
        selectedAspectRatio;

    if (
        job.planner_provider_snapshot
        &&
        job.planner_model_snapshot
    ) {
        summaryPlanner.textContent =
            `${capitalize(job.planner_provider_snapshot)} · ${job.planner_model_snapshot}`;
    }

    if (
        job.image_provider_snapshot
        &&
        job.image_model_snapshot
    ) {
        summaryImageEngine.textContent =
            `${capitalize(job.image_provider_snapshot)} · ${job.image_model_snapshot}`;
    }

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

    updateNewGenerationButton();
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

    let keepPolling =
        false;

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

        const dispatch =
            await response.json();

        if (
            dispatch.status
            ===
            "queued"
        ) {
            keepPolling =
                true;

            startImageBatchPolling(
                jobId
            );

            setPipelineStep(
                pipelineImages,
                "active",
                "Queued"
            );

            jobPanelStatus.textContent =
                "QUEUED";

            showToast(
                "Generation queued. You can leave this page; Hyperex will continue processing it."
            );

            return true;
        }

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

        if (!keepPolling) {
            stopImageBatchPolling();
        }
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
   DELETE / CLEANUP
========================================================= */

async function deleteGeneratedImageFromApp(
    imageId,
    jobId
) {
    const confirmed =
        window.confirm(
            "Delete this generated image? This cannot be undone."
        );

    if (!confirmed) {
        return false;
    }

    try {
        const response =
            await fetch(
                `/api/images/${imageId}`,
                {
                    method:
                        "DELETE",
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

        if (
            currentJob
            &&
            Number(
                currentJob.id
            )
            ===
            Number(
                jobId
            )
        ) {
            await refreshImageBatch(
                currentJob.id
            );
        }

        if (
            historyDetail
            &&
            Number(
                historyDetail.id
            )
            ===
            Number(
                jobId
            )
        ) {
            await openHistoryJob(
                historyDetail.id,
                {
                    preserveModal:
                        true,
                }
            );
        }

        if (
            !historyView.classList.contains(
                "hidden-view"
            )
        ) {
            await loadHistory();
        }

        showToast(
            "Image deleted."
        );

        return true;

    } catch (error) {
        showToast(
            error.message
        );

        return false;
    }
}


function resetCurrentJobView() {
    stopImageBatchPolling();

    currentJob =
        null;

    currentPromptPackages =
        [];

    lastRenderedBatch =
        null;

    selectedCompareIds.clear();

    localStorage.removeItem(
        LAST_JOB_KEY
    );

    jobSavedState.classList.add(
        "hidden-element"
    );

    jobEmptyState.classList.remove(
        "hidden-element"
    );

    jobPanelStatus.textContent =
        "DRAFT";

    pipelineSection.classList.add(
        "hidden-element"
    );

    imageBatchSection.classList.add(
        "hidden-element"
    );

    resultsSection.classList.add(
        "hidden-element"
    );

    plannerResultSection.classList.add(
        "hidden-element"
    );

    promptPackagesSection.classList.add(
        "hidden-element"
    );

    storedReferenceGrid.innerHTML =
        "";

    plannerRawOutput.textContent =
        "";

    promptPackageGrid.innerHTML =
        "";

    imageBatchGrid.innerHTML =
        "";

    resultsGrid.innerHTML =
        "";

    updateNewGenerationButton();
}


function updateNewGenerationButton() {
    if (!newGenerationButton) {
        return;
    }

    const complete =
        Number(
            lastRenderedBatch
                ?.complete_count
            ||
            0
        );

    const active =
        Number(
            lastRenderedBatch
                ?.generating_count
            ||
            0
        )
        +
        Number(
            lastRenderedBatch
                ?.queued_count
            ||
            0
        );

    const available =
        Boolean(
            currentJob
        )
        &&
        complete > 0
        &&
        active === 0;

    newGenerationButton.classList.toggle(
        "hidden-element",
        !available
    );

    newGenerationButton.disabled =
        !available;
}


function startNewGenerationWorkspace() {
    if (
        !currentJob
        ||
        !lastRenderedBatch
    ) {
        return;
    }

    const complete =
        Number(
            lastRenderedBatch.complete_count
            ||
            0
        );

    const active =
        Number(
            lastRenderedBatch.generating_count
            ||
            0
        )
        +
        Number(
            lastRenderedBatch.queued_count
            ||
            0
        );

    if (
        complete < 1
        ||
        active > 0
    ) {
        return;
    }

    /*
     * Preserve:
     * - selected workflow
     * - output count
     * - aspect ratio
     * - auto-generate choice
     * - Planner/Image provider + quality settings
     *
     * Clear only project/job-specific Create state.
     */

    selectedImages =
        [];

    replaceTargetIndex =
        null;

    draggedReferenceIndex =
        null;

    activeFinalPackage =
        null;

    previewResults =
        [];

    previewPackageLookup =
        [];

    previewJobId =
        null;

    regenerateTarget =
        null;

    regenerateJobId =
        null;

    description.value =
        "";

    characterCount.textContent =
        "0 characters";

    imageInput.value =
        "";

    replaceImageInput.value =
        "";

    /*
     * Remove the old content draft so the previous description
     * cannot come back after refresh.
     */
    localStorage.removeItem(
        CREATE_DRAFT_KEY
    );

    resetPipeline();
    resetCurrentJobView();
    renderReferenceCards();

    /*
     * Save only the retained workflow/count/ratio choices
     * with an empty description.
     */
    saveCreateDraft();

    showToast(
        "New generation ready. Add your new references."
    );

    requestAnimationFrame(
        () => {
            uploadZone.scrollIntoView({
                behavior:
                    "smooth",
                block:
                    "center",
            });
        }
    );
}


if (newGenerationButton) {
    newGenerationButton.addEventListener(
        "click",
        startNewGenerationWorkspace
    );
}


async function deleteJobFromApp(
    jobId
) {
    const confirmed =
        window.confirm(
            `Delete Job #${jobId} and its saved references/images? This cannot be undone.`
        );

    if (!confirmed) {
        return false;
    }

    try {
        const response =
            await fetch(
                `/api/jobs/${jobId}`,
                {
                    method:
                        "DELETE",
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

        if (
            currentJob
            &&
            Number(
                currentJob.id
            )
            ===
            Number(
                jobId
            )
        ) {
            resetCurrentJobView();
        }

        if (
            historyDetail
            &&
            Number(
                historyDetail.id
            )
            ===
            Number(
                jobId
            )
        ) {
            historyDetail =
                null;

            closeModal(
                historyDetailModal
            );
        }

        await loadHistory();

        showToast(
            "Job deleted."
        );

        return true;

    } catch (error) {
        showToast(
            error.message
        );

        return false;
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

    const remove =
        document.createElement(
            "button"
        );

    remove.type =
        "button";

    remove.className =
        "result-delete-button";

    remove.textContent =
        "Delete";

    remove.onclick =
        () =>
            deleteGeneratedImageFromApp(
                item.image.id,
                currentJob?.id
            );

    actions.append(
        view,
        regenerate,
        download,
        remove
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

            const dispatch =
                await response.json();

            closeModal(
                regenerateModal
            );

            if (
                dispatch.status
                ===
                "queued"
            ) {
                if (
                    currentJob
                    &&
                    Number(currentJob.id)
                    ===
                    Number(regenerateJobId)
                ) {
                    startImageBatchPolling(
                        currentJob.id
                    );
                }

                showToast(
                    "Regeneration queued. Hyperex will update the job when it finishes."
                );

                return;
            }

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

    historyDetailRatio.textContent =
        detail.aspect_ratio
        ||
        "1:1";

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

    const remove =
        document.createElement(
            "button"
        );

    remove.type =
        "button";

    remove.className =
        "result-delete-button";

    remove.textContent =
        "Delete";

    remove.onclick =
        () =>
            deleteGeneratedImageFromApp(
                item.image.id,
                detail.id
            );

    actions.append(
        view,
        prompt,
        download,
        remove
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


historyDeleteJobButton.addEventListener(
    "click",
    async () => {
        if (!historyDetail) {
            return;
        }

        await deleteJobFromApp(
            historyDetail.id
        );
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

        setSelectedAspectRatio(
            detail.aspect_ratio
            ||
            "1:1"
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
    value,
    saveDraft = true
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

    if (saveDraft) {
        saveCreateDraft();
    }
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
                profile.workflow_type
                ===
                "private"
            ) {
                button.classList.add(
                    "private-workflow"
                );
            }

            if (
                profile.workflow_type
                ===
                "template"
            ) {
                button.classList.add(
                    "template-workflow"
                );
            }

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
                isManagedProfile(
                    profile
                )
                    ?
                    (
                        profile.workflow_type
                        ===
                        "template"
                            ?
                            "HYPEREX · PUBLIC TEMPLATE"
                            :
                            "HYPEREX · PRIVATE"
                    )
                    :
                    (
                        Number(
                            profile.is_active
                        )
                        ===
                        1
                            ?
                            "MY PROFILE · ACTIVE"
                            :
                            "MY PROFILE · ARCHIVED"
                    );

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

        const managed =
            isManagedProfile(
                profile
            );

        const privateManaged =
            managed
            &&
            profile.workflow_type
            ===
            "private";

        const templateManaged =
            managed
            &&
            profile.workflow_type
            ===
            "template";

        profileInstructionEditor.value =
            privateManaged
                ?
                ""
                :
                (
                    profile.system_instruction
                    ||
                    ""
                );

        instructionCharacterCount.textContent =
            privateManaged
                ?
                "Private instruction"
                :
                `${formatNumber(profileInstructionEditor.value.length)} characters`;

        privateProfileNotice.classList.toggle(
            "hidden-element",
            !managed
        );

        if (managed) {
            const noticeTitle =
                privateProfileNotice.querySelector(
                    "strong"
                );

            const noticeCopy =
                privateProfileNotice.querySelector(
                    "span"
                );

            if (privateManaged) {
                noticeTitle.textContent =
                    "HYPEREX PRIVATE WORKFLOW";

                noticeCopy.textContent =
                    (
                        "You can use this workflow for generation, but its "
                        +
                        "system instruction is managed privately by Hyperex."
                    );
            } else {
                noticeTitle.textContent =
                    "HYPEREX PUBLIC TEMPLATE";

                noticeCopy.textContent =
                    (
                        "The shared template is read-only. Use Customize Template "
                        +
                        "to create your own editable copy."
                    );
            }
        }

        const active =
            Number(
                profile.is_active
            )
            ===
            1;

        if (managed) {
            profileStateBadge.textContent =
                templateManaged
                    ?
                    "HYPEREX · TEMPLATE"
                    :
                    "HYPEREX · PRIVATE";
        } else {
            profileStateBadge.textContent =
                active
                    ?
                    "MY PROFILE · ACTIVE"
                    :
                    "MY PROFILE · ARCHIVED";
        }

        customizeTemplateButton.classList.toggle(
            "hidden-element",
            !templateManaged
        );

        archiveProfileButton.classList.toggle(
            "hidden-element",
            !active
            ||
            managed
        );

        restoreProfileButton.classList.toggle(
            "hidden-element",
            active
            ||
            managed
        );

        deleteProfileButton.classList.toggle(
            "hidden-element",
            managed
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
                    !active
                    ||
                    managed;
            }
        );

        profileInstructionEditor.placeholder =
            privateManaged
                ?
                "Private Hyperex workflow instruction."
                :
                templateManaged
                    ?
                    "Public template instruction. Customize it to edit your own copy."
                    :
                    "";

        renderManagerProfiles();

    } catch (error) {
        showToast(
            error.message
        );
    }
}


customizeTemplateButton.addEventListener(
    "click",
    async () => {
        if (!editingProfileId) {
            return;
        }

        customizeTemplateButton.disabled =
            true;

        customizeTemplateButton.textContent =
            "Creating copy…";

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}/customize`,
                    {
                        method:
                            "POST",
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

            showToast(
                "Editable copy created in My Profiles."
            );

            await Promise.all([
                loadProfiles(
                    profile.id
                ),
                loadManagerProfiles(),
            ]);

            await openProfileEditor(
                profile.id
            );

        } catch (error) {
            showToast(
                error.message
            );

        } finally {
            customizeTemplateButton.disabled =
                false;

            customizeTemplateButton.textContent =
                "Customize template";
        }
    }
);


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
    changePasswordModal,
    adminWorkflowModal,
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


closeAdminWorkflowModal.addEventListener(
    "click",
    () =>
        closeModal(
            adminWorkflowModal
        )
);


cancelAdminWorkflowButton.addEventListener(
    "click",
    () =>
        closeModal(
            adminWorkflowModal
        )
);


closeChangePasswordModal.addEventListener(
    "click",
    () =>
        closeModal(
            changePasswordModal
        )
);


cancelChangePasswordButton.addEventListener(
    "click",
    () =>
        closeModal(
            changePasswordModal
        )
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
                changePasswordModal,
                adminWorkflowModal,
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

    setSelectedAspectRatio(
        selectedAspectRatio
    );

    await Promise.all([
        loadSettings(),
        loadProfiles(),
    ]);

    const restoredDraft =
        restoreCreateDraft();

    renderReferenceCards();

    const restoredJob =
        await restoreLastJob();

    if (
        restoredDraft
        &&
        !selectedImages.length
    ) {
        showToast(
            "Draft restored. Re-add reference images when ready."
        );
    } else if (restoredJob) {
        showToast(
            "Unfinished job restored."
        );
    }

    if (
        "serviceWorker"
        in
        navigator
    ) {
        navigator
            .serviceWorker
            .register(
                "/static/service-worker.js"
            )
            .catch(
                error =>
                    console.warn(
                        "Service worker registration failed:",
                        error
                    )
            );
    }
}


bootApplication();
