const navGenerate =
    document.getElementById("navGenerate");

const navProfiles =
    document.getElementById("navProfiles");

const navHistory =
    document.getElementById("navHistory");

const navSettings =
    document.getElementById("navSettings");

const generateView =
    document.getElementById("generateView");

const profilesView =
    document.getElementById("profilesView");

const settingsView =
    document.getElementById("settingsView");


const profileOptions =
    document.getElementById("profileOptions");

const imageInput =
    document.getElementById("imageInput");

const uploadZone =
    document.getElementById("uploadZone");

const imagePreviewGrid =
    document.getElementById("imagePreviewGrid");

const description =
    document.getElementById("description");

const characterCount =
    document.getElementById("characterCount");

const summaryProfile =
    document.getElementById("summaryProfile");

const summaryVersion =
    document.getElementById("summaryVersion");

const summaryImages =
    document.getElementById("summaryImages");

const summaryCount =
    document.getElementById("summaryCount");

const generateButton =
    document.getElementById("generateButton");

const generateButtonLabel =
    document.getElementById("generateButtonLabel");

const generateButtonArrow =
    document.getElementById("generateButtonArrow");

const jobPanelStatus =
    document.getElementById("jobPanelStatus");

const jobEmptyState =
    document.getElementById("jobEmptyState");

const jobSavedState =
    document.getElementById("jobSavedState");

const currentJobId =
    document.getElementById("currentJobId");

const storedReferenceGrid =
    document.getElementById("storedReferenceGrid");


const newProfileButton =
    document.getElementById("newProfileButton");

const libraryCount =
    document.getElementById("libraryCount");

const profileSearch =
    document.getElementById("profileSearch");

const profileManagerList =
    document.getElementById("profileManagerList");

const profileEditorEmpty =
    document.getElementById("profileEditorEmpty");

const profileEditorContent =
    document.getElementById("profileEditorContent");

const profileEditorTitle =
    document.getElementById("profileEditorTitle");

const profileStateBadge =
    document.getElementById("profileStateBadge");

const activeVersionBadge =
    document.getElementById("activeVersionBadge");

const latestVersionBadge =
    document.getElementById("latestVersionBadge");

const loadedVersionBadge =
    document.getElementById("loadedVersionBadge");

const loadedVersionNote =
    document.getElementById("loadedVersionNote");

const profileNameInput =
    document.getElementById("profileNameInput");

const profileDescriptionInput =
    document.getElementById("profileDescriptionInput");

const profileInstructionEditor =
    document.getElementById("profileInstructionEditor");

const instructionCharacterCount =
    document.getElementById("instructionCharacterCount");

const saveDetailsButton =
    document.getElementById("saveDetailsButton");

const saveVersionButton =
    document.getElementById("saveVersionButton");

const archiveProfileButton =
    document.getElementById("archiveProfileButton");

const restoreProfileButton =
    document.getElementById("restoreProfileButton");

const deleteProfileButton =
    document.getElementById("deleteProfileButton");

const versionHistoryList =
    document.getElementById("versionHistoryList");


const geminiProviderStatus =
    document.getElementById("geminiProviderStatus");

const geminiModel =
    document.getElementById("geminiModel");

const geminiKeyStatus =
    document.getElementById("geminiKeyStatus");

const geminiKeySource =
    document.getElementById("geminiKeySource");

const geminiSdkVersion =
    document.getElementById("geminiSdkVersion");

const geminiStorageMode =
    document.getElementById("geminiStorageMode");

const testGeminiButton =
    document.getElementById("testGeminiButton");

const geminiTestResult =
    document.getElementById("geminiTestResult");


const newProfileModal =
    document.getElementById("newProfileModal");

const modalCloseButton =
    document.getElementById("modalCloseButton");

const cancelCreateProfile =
    document.getElementById("cancelCreateProfile");

const newProfileForm =
    document.getElementById("newProfileForm");

const newProfileName =
    document.getElementById("newProfileName");

const newProfileDescription =
    document.getElementById("newProfileDescription");

const newProfileInstruction =
    document.getElementById("newProfileInstruction");

const newInstructionCharacterCount =
    document.getElementById("newInstructionCharacterCount");

const createProfileButton =
    document.getElementById("createProfileButton");

const toast =
    document.getElementById("toast");


let profiles = [];
let managerProfiles = [];
let selectedProfileId = null;
let selectedProfileVersionId = null;
let selectedImages = [];
let selectedCount = "auto";
let editingProfileId = null;
let editingProfileName = null;
let loadedEditorVersionNumber = null;
let currentJob = null;
let toastTimer = null;


function showView(view) {
    generateView.classList.toggle(
        "hidden-view",
        view !== "generate"
    );

    profilesView.classList.toggle(
        "hidden-view",
        view !== "profiles"
    );

    settingsView.classList.toggle(
        "hidden-view",
        view !== "settings"
    );

    navGenerate.classList.toggle(
        "active",
        view === "generate"
    );

    navProfiles.classList.toggle(
        "active",
        view === "profiles"
    );

    navSettings.classList.toggle(
        "active",
        view === "settings"
    );
}


navGenerate.addEventListener(
    "click",
    () => showView("generate")
);


navProfiles.addEventListener(
    "click",
    async () => {

        showView("profiles");

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


navSettings.addEventListener(
    "click",
    async () => {

        showView("settings");

        await loadGeminiStatus();
    }
);


navHistory.addEventListener(
    "click",
    () => {

        showToast(
            "History will be added after the AI generation flow."
        );
    }
);


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
            return data.detail;
        }
    } catch {
        // Ignore JSON parsing errors.
    }

    return (
        `Request failed (${response.status})`
    );
}


/* =========================================================
   GEMINI SETTINGS
========================================================= */

async function loadGeminiStatus() {
    geminiProviderStatus.textContent =
        "CHECKING";

    geminiProviderStatus.classList.remove(
        "ready"
    );

    try {
        const response =
            await fetch(
                "/api/providers/gemini/status"
            );

        if (!response.ok) {
            throw new Error(
                await apiError(response)
            );
        }

        const status =
            await response.json();

        geminiModel.textContent =
            status.model
            ||
            "—";

        geminiKeyStatus.textContent =
            status.configured
                ?
                "CONFIGURED"
                :
                "NOT CONFIGURED";

        geminiKeySource.textContent =
            status.key_source
            ||
            "—";

        geminiSdkVersion.textContent =
            status.sdk_version
            ||
            "—";

        geminiStorageMode.textContent =
            status.store_interactions
                ?
                "ON"
                :
                "OFF";

        geminiProviderStatus.textContent =
            status.configured
                ?
                "CONFIGURED"
                :
                "NEEDS KEY";

        geminiProviderStatus.classList.toggle(
            "ready",
            Boolean(
                status.configured
            )
        );

        if (!status.configured) {
            geminiTestResult.classList.remove(
                "success"
            );

            geminiTestResult.textContent =
                "Create a project .env file, add GEMINI_API_KEY, restart FastAPI, then test again.";
        }

    } catch (error) {
        console.error(error);

        geminiProviderStatus.textContent =
            "ERROR";

        geminiTestResult.classList.remove(
            "success"
        );

        geminiTestResult.textContent =
            error.message;
    }
}


testGeminiButton.addEventListener(
    "click",
    async () => {

        testGeminiButton.disabled =
            true;

        testGeminiButton.textContent =
            "TESTING CONNECTION...";

        geminiTestResult.classList.remove(
            "success"
        );

        geminiTestResult.textContent =
            "Sending a small stateless request to Gemini...";

        try {
            const response =
                await fetch(
                    "/api/providers/gemini/test",
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {
                throw new Error(
                    await apiError(response)
                );
            }

            const result =
                await response.json();

            geminiTestResult.classList.add(
                "success"
            );

            geminiTestResult.textContent =
                `Connection successful. ${result.model} replied: ${result.response}`;

            await loadGeminiStatus();

            showToast(
                "Gemini connection successful."
            );

        } catch (error) {
            console.error(error);

            geminiTestResult.classList.remove(
                "success"
            );

            geminiTestResult.textContent =
                error.message;

            showToast(
                "Gemini connection test failed."
            );

        } finally {
            testGeminiButton.disabled =
                false;

            testGeminiButton.textContent =
                "TEST GEMINI CONNECTION";
        }
    }
);


/* =========================================================
   GENERATE PROFILES
========================================================= */

async function loadProfiles(
    preferredId = selectedProfileId
) {
    profileOptions.innerHTML = `
        <div class="loading-state">
            Loading profiles...
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
        console.error(error);

        profileOptions.innerHTML = `
            <div class="loading-state">
                Could not load profiles.
            </div>
        `;
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
                No active profiles.
            </div>
        `;

        selectedProfileId =
            null;

        selectedProfileVersionId =
            null;

        summaryProfile.textContent =
            "No profile";

        summaryVersion.textContent =
            "—";

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

    let chosen =
        profiles.find(
            item =>
                Number(item.id)
                ===
                Number(preferredId)
        );

    if (!chosen) {
        chosen =
            profiles[0];
    }

    selectGenerateProfile(
        chosen.id
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
        profile.id;

    const radio =
        document.createElement(
            "input"
        );

    radio.type =
        "radio";

    radio.name =
        "profile";

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

    const detail =
        document.createElement(
            "span"
        );

    const active =
        profile.active_version_number;

    const latest =
        profile.latest_version_number;

    if (
        active
        ===
        latest
    ) {
        detail.textContent =
            `Using v${active} · ${profile.description || "No description"}`;
    } else {
        detail.textContent =
            `Using v${active} · Latest v${latest} · ${profile.description || "No description"}`;
    }

    const check =
        document.createElement(
            "div"
        );

    check.className =
        "profile-check";

    check.textContent =
        "●";

    text.append(
        title,
        detail
    );

    card.append(
        radio,
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
        );

    document
        .querySelectorAll(
            ".profile-card"
        )
        .forEach(
            card => {

                const selected =
                    Number(
                        card.dataset.profileId
                    )
                    ===
                    selectedProfileId;

                card.classList.toggle(
                    "active-profile",
                    selected
                );

                const radio =
                    card.querySelector(
                        "input"
                    );

                if (radio) {
                    radio.checked =
                        selected;
                }
            }
        );

    summaryProfile.textContent =
        profile.name;

    summaryVersion.textContent =
        `v${profile.active_version_number}`;

    markDraftChanged();
}


/* =========================================================
   MANAGER
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
        console.error(error);

        profileManagerList.innerHTML = `
            <div class="loading-state">
                Could not load profiles.
            </div>
        `;
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

                const text =
                    `${profile.name} ${profile.description || ""}`
                        .toLowerCase();

                return text.includes(
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

            const titleRow =
                document.createElement(
                    "div"
                );

            titleRow.className =
                "manager-profile-title-row";

            const title =
                document.createElement(
                    "div"
                );

            title.className =
                "manager-profile-title";

            title.textContent =
                profile.name;

            const version =
                document.createElement(
                    "span"
                );

            version.className =
                "manager-profile-version";

            version.textContent =
                `v${profile.active_version_number}`;

            titleRow.append(
                title,
                version
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
                    `ACTIVE · GENERATE v${profile.active_version_number}`
                    :
                    "ARCHIVED";

            button.append(
                titleRow,
                desc,
                status
            );

            button.addEventListener(
                "click",
                () => {

                    openProfileEditor(
                        profile.id
                    );
                }
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
    profileId,
    versionNumber = null
) {
    try {
        let url =
            `/api/profiles/${profileId}`;

        if (
            versionNumber
            !==
            null
        ) {
            url =
                `/api/profiles/${profileId}/versions/${versionNumber}`;
        }

        const response =
            await fetch(
                url
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

        loadedEditorVersionNumber =
            Number(
                profile.version_number
            );

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

        activeVersionBadge.textContent =
            `v${profile.active_version_number}`;

        latestVersionBadge.textContent =
            `v${profile.latest_version_number}`;

        loadedVersionBadge.textContent =
            `v${profile.version_number}`;

        if (
            Number(
                profile.version_number
            )
            ===
            Number(
                profile.active_version_number
            )
        ) {
            loadedVersionNote.textContent =
                `v${profile.version_number} is currently used by Generate.`;
        } else {
            loadedVersionNote.textContent =
                `You are editing v${profile.version_number}. Generate currently uses v${profile.active_version_number}.`;
        }

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

        profileNameInput.disabled =
            !active;

        profileDescriptionInput.disabled =
            !active;

        profileInstructionEditor.disabled =
            !active;

        saveDetailsButton.disabled =
            !active;

        saveVersionButton.disabled =
            !active;

        updateInstructionCount();

        renderManagerProfiles();

        await loadVersionHistory(
            editingProfileId
        );

    } catch (error) {
        console.error(error);

        showToast(
            error.message
        );
    }
}


async function loadVersionHistory(
    profileId
) {
    versionHistoryList.innerHTML = `
        <div class="loading-state">
            Loading versions...
        </div>
    `;

    try {
        const response =
            await fetch(
                `/api/profiles/${profileId}/versions`
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

        const versions =
            Array.isArray(
                data.versions
            )
                ?
                data.versions
                :
                [];

        versionHistoryList.innerHTML =
            "";

        versions.forEach(
            version => {

                versionHistoryList.appendChild(
                    createVersionRow(
                        profileId,
                        version,
                        versions.length
                    )
                );
            }
        );

    } catch (error) {
        console.error(error);

        versionHistoryList.innerHTML = `
            <div class="loading-state">
                Could not load versions.
            </div>
        `;
    }
}


function createVersionRow(
    profileId,
    version,
    totalVersions
) {
    const row =
        document.createElement(
            "div"
        );

    row.className =
        "version-row";

    const isGenerationVersion =
        Number(
            version.is_generation_version
        )
        ===
        1;

    if (isGenerationVersion) {
        row.classList.add(
            "generation-version"
        );
    }

    const info =
        document.createElement(
            "div"
        );

    info.className =
        "version-row-info";

    const title =
        document.createElement(
            "strong"
        );

    title.textContent =
        `Version ${version.version_number}`;

    const meta =
        document.createElement(
            "div"
        );

    meta.className =
        "version-row-meta";

    meta.innerHTML = `
        <span>${formatDate(version.created_at)}</span>
        <span>${formatNumber(version.character_count)} characters</span>
    `;

    info.append(
        title,
        meta
    );

    if (isGenerationVersion) {
        const activeLabel =
            document.createElement(
                "span"
            );

        activeLabel.className =
            "version-active-label";

        activeLabel.textContent =
            "USED BY GENERATE";

        info.appendChild(
            activeLabel
        );
    }

    const actions =
        document.createElement(
            "div"
        );

    actions.className =
        "version-actions";

    const loadButton =
        document.createElement(
            "button"
        );

    loadButton.className =
        "version-action";

    loadButton.type =
        "button";

    const isLoaded =
        Number(
            version.version_number
        )
        ===
        Number(
            loadedEditorVersionNumber
        );

    loadButton.textContent =
        isLoaded
            ?
            "LOADED"
            :
            "LOAD";

    loadButton.disabled =
        isLoaded;

    loadButton.addEventListener(
        "click",
        () => {

            openProfileEditor(
                profileId,
                version.version_number
            );
        }
    );

    const useButton =
        document.createElement(
            "button"
        );

    useButton.className =
        "version-action primary";

    useButton.type =
        "button";

    useButton.textContent =
        isGenerationVersion
            ?
            "IN GENERATE"
            :
            "USE FOR GENERATE";

    useButton.disabled =
        isGenerationVersion;

    useButton.addEventListener(
        "click",
        async () => {

            await activateVersion(
                profileId,
                version.version_number
            );
        }
    );

    const deleteButton =
        document.createElement(
            "button"
        );

    deleteButton.className =
        "version-action delete";

    deleteButton.type =
        "button";

    deleteButton.textContent =
        "DELETE";

    const usedByJobs =
        Number(
            version.usage_count
        )
        >
        0;

    deleteButton.disabled =
        isGenerationVersion
        ||
        totalVersions <= 1
        ||
        usedByJobs;

    deleteButton.addEventListener(
        "click",
        async () => {

            await deleteVersion(
                profileId,
                version.version_number
            );
        }
    );

    actions.append(
        loadButton,
        useButton,
        deleteButton
    );

    row.append(
        info,
        actions
    );

    return row;
}


async function activateVersion(
    profileId,
    versionNumber
) {
    const confirmed =
        window.confirm(
            `Use version ${versionNumber} for Generate?`
        );

    if (!confirmed) {
        return;
    }

    try {
        const response =
            await fetch(
                `/api/profiles/${profileId}/versions/${versionNumber}/activate`,
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

        await loadProfiles(
            profileId
        );

        await loadManagerProfiles();

        await openProfileEditor(
            profileId,
            versionNumber
        );

        showToast(
            `Generate now uses version ${versionNumber}.`
        );

    } catch (error) {
        console.error(error);

        showToast(
            error.message
        );
    }
}


async function deleteVersion(
    profileId,
    versionNumber
) {
    const confirmed =
        window.confirm(
            `Delete version ${versionNumber} permanently?\n\nThis cannot be undone.`
        );

    if (!confirmed) {
        return;
    }

    try {
        const response =
            await fetch(
                `/api/profiles/${profileId}/versions/${versionNumber}`,
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

        await loadProfiles(
            profileId
        );

        await loadManagerProfiles();

        await openProfileEditor(
            profileId
        );

        showToast(
            `Version ${versionNumber} deleted.`
        );

    } catch (error) {
        console.error(error);

        showToast(
            error.message
        );
    }
}


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
                        method: "PATCH",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                name,

                                description:
                                    profileDescriptionInput
                                        .value
                                        .trim()
                            })
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
                editingProfileId,
                loadedEditorVersionNumber
            );

            showToast(
                "Profile details saved."
            );

        } catch (error) {
            console.error(error);

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

        const confirmed =
            window.confirm(
                "Save this instruction as a new version?\n\nThe new version will automatically become the version used by Generate."
            );

        if (!confirmed) {
            return;
        }

        try {
            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}/versions`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                system_instruction:
                                    instruction
                            })
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

            await loadProfiles(
                editingProfileId
            );

            await loadManagerProfiles();

            await openProfileEditor(
                editingProfileId
            );

            showToast(
                `Version ${updated.version_number} created and activated.`
            );

        } catch (error) {
            console.error(error);

            showToast(
                error.message
            );
        }
    }
);


archiveProfileButton.addEventListener(
    "click",
    async () => {

        if (!editingProfileId) {
            return;
        }

        const confirmed =
            window.confirm(
                `Archive "${editingProfileName}"?\n\nIt will disappear from Generate but remain saved.`
            );

        if (!confirmed) {
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
            console.error(error);

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
            console.error(error);

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
                `Permanent deletion cannot be undone.\n\nType the profile name exactly to continue:\n\n${editingProfileName}`
            );

        if (
            typed
            !==
            editingProfileName
        ) {
            if (
                typed
                !==
                null
            ) {
                showToast(
                    "Profile name did not match. Nothing was deleted."
                );
            }

            return;
        }

        const finalConfirm =
            window.confirm(
                `Delete "${editingProfileName}" permanently?`
            );

        if (!finalConfirm) {
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

            loadedEditorVersionNumber =
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
                "Profile permanently deleted."
            );

        } catch (error) {
            console.error(error);

            showToast(
                error.message
            );
        }
    }
);


function updateInstructionCount() {
    const length =
        profileInstructionEditor
            .value
            .length;

    instructionCharacterCount.textContent =
        `${formatNumber(length)} ${
            length === 1
                ?
                "character"
                :
                "characters"
        }`;
}


profileInstructionEditor.addEventListener(
    "input",
    updateInstructionCount
);


/* =========================================================
   CREATE PROFILE MODAL
========================================================= */

function openModal() {
    newProfileForm.reset();

    newInstructionCharacterCount.textContent =
        "0 characters";

    newProfileModal.classList.add(
        "visible"
    );

    newProfileModal.setAttribute(
        "aria-hidden",
        "false"
    );
}


function closeModal() {
    newProfileModal.classList.remove(
        "visible"
    );

    newProfileModal.setAttribute(
        "aria-hidden",
        "true"
    );
}


newProfileButton.addEventListener(
    "click",
    openModal
);


modalCloseButton.addEventListener(
    "click",
    closeModal
);


cancelCreateProfile.addEventListener(
    "click",
    closeModal
);


newProfileModal.addEventListener(
    "click",
    event => {

        if (
            event.target
            ===
            newProfileModal
        ) {
            closeModal();
        }
    }
);


newProfileInstruction.addEventListener(
    "input",
    () => {

        const length =
            newProfileInstruction
                .value
                .length;

        newInstructionCharacterCount.textContent =
            `${formatNumber(length)} characters`;
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
                "Profile name and system instruction are required."
            );

            return;
        }

        try {
            const response =
                await fetch(
                    "/api/profiles",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                name,

                                description:
                                    newProfileDescription
                                        .value
                                        .trim(),

                                system_instruction:
                                    instruction
                            })
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

            closeModal();

            await loadProfiles(
                profile.id
            );

            await loadManagerProfiles();

            await openProfileEditor(
                profile.id
            );

            showToast(
                `${profile.name} created.`
            );

        } catch (error) {
            console.error(error);

            showToast(
                error.message
            );
        }
    }
);


/* =========================================================
   IMAGE UPLOAD / JOB PREP
========================================================= */

uploadZone.addEventListener(
    "click",
    () => imageInput.click()
);


imageInput.addEventListener(
    "change",
    event => {

        addImages(
            event.target.files
        );
    }
);


uploadZone.addEventListener(
    "dragover",
    event => {

        event.preventDefault();

        uploadZone.classList.add(
            "dragging"
        );
    }
);


uploadZone.addEventListener(
    "dragleave",
    () => {

        uploadZone.classList.remove(
            "dragging"
        );
    }
);


uploadZone.addEventListener(
    "drop",
    event => {

        event.preventDefault();

        uploadZone.classList.remove(
            "dragging"
        );

        addImages(
            event.dataTransfer.files
        );
    }
);


function addImages(
    files
) {
    const images =
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
        of images
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

    renderImages();

    imageInput.value =
        "";

    markDraftChanged();
}


function renderImages() {
    imagePreviewGrid.innerHTML =
        "";

    selectedImages.forEach(
        (
            file,
            index
        ) => {

            const preview =
                document.createElement(
                    "div"
                );

            preview.className =
                "image-preview";

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

            image.addEventListener(
                "load",
                () => {

                    URL.revokeObjectURL(
                        url
                    );
                },
                {
                    once: true
                }
            );

            const number =
                document.createElement(
                    "span"
                );

            number.className =
                "image-number";

            number.textContent =
                `Image ${index + 1}`;

            const remove =
                document.createElement(
                    "button"
                );

            remove.type =
                "button";

            remove.className =
                "remove-image";

            remove.textContent =
                "×";

            remove.addEventListener(
                "click",
                () => {

                    selectedImages.splice(
                        index,
                        1
                    );

                    renderImages();

                    markDraftChanged();
                }
            );

            preview.append(
                image,
                number,
                remove
            );

            imagePreviewGrid.appendChild(
                preview
            );
        }
    );

    summaryImages.textContent =
        String(
            selectedImages.length
        );
}


description.addEventListener(
    "input",
    () => {

        const length =
            description
                .value
                .length;

        characterCount.textContent =
            `${length} characters`;

        markDraftChanged();
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
                            item => {

                                item.classList.remove(
                                    "selected"
                                );
                            }
                        );

                    button.classList.add(
                        "selected"
                    );

                    selectedCount =
                        button.dataset.count;

                    summaryCount.textContent =
                        selectedCount
                        ===
                        "auto"
                            ?
                            "Auto"
                            :
                            selectedCount;

                    markDraftChanged();
                }
            );
        }
    );


generateButton.addEventListener(
    "click",
    prepareGenerationJob
);


async function prepareGenerationJob() {
    if (!selectedProfileId) {
        showToast(
            "Select a profile first."
        );

        return;
    }

    if (!selectedImages.length) {
        showToast(
            "Add at least one reference image."
        );

        return;
    }

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
        description
            .value
            .trim()
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

    setGenerateBusy(
        true
    );

    jobPanelStatus.textContent =
        "SAVING";

    try {
        const response =
            await fetch(
                "/api/jobs",
                {
                    method: "POST",
                    body: formData
                }
            );

        if (!response.ok) {
            throw new Error(
                await apiError(
                    response
                )
            );
        }

        const job =
            await response.json();

        currentJob =
            job;

        renderPreparedJob(
            job
        );

        showToast(
            `Job #${job.id} saved with ${job.reference_count} reference image${job.reference_count === 1 ? "" : "s"}.`
        );

    } catch (error) {
        console.error(error);

        jobPanelStatus.textContent =
            currentJob
                ?
                "DRAFT CHANGED"
                :
                "DRAFT";

        showToast(
            error.message
        );

    } finally {
        setGenerateBusy(
            false
        );
    }
}


function setGenerateBusy(
    busy
) {
    generateButton.disabled =
        busy;

    if (busy) {
        generateButtonLabel.textContent =
            "SAVING REFERENCES";

        generateButtonArrow.textContent =
            "…";
    } else {
        generateButtonLabel.textContent =
            "GENERATE IMAGES";

        generateButtonArrow.textContent =
            "→";
    }
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

    jobPanelStatus.textContent =
        "PREPARED";

    currentJobId.textContent =
        `#${String(job.id).padStart(4, "0")}`;

    summaryProfile.textContent =
        job.profile_name;

    summaryVersion.textContent =
        `v${job.profile_version_number}`;

    summaryImages.textContent =
        String(
            job.reference_count
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

    job.references.forEach(
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
                String(
                    reference.position
                );

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


function markDraftChanged() {
    if (!currentJob) {
        return;
    }

    jobPanelStatus.textContent =
        "DRAFT CHANGED";
}


/* =========================================================
   HELPERS
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


function formatDate(
    value
) {
    if (!value) {
        return "Unknown date";
    }

    const date =
        new Date(
            value.replace(
                " ",
                "T"
            )
            +
            "Z"
        );

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {
        return value;
    }

    return date.toLocaleString();
}


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
            3200
        );
}


/* =========================================================
   START
========================================================= */

async function startApplication() {
    showView(
        "generate"
    );

    await loadProfiles();
}


startApplication();
