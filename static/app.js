/* =========================================================
   DOM — NAVIGATION
========================================================= */

const navGenerate =
    document.getElementById(
        "navGenerate"
    );

const navProfiles =
    document.getElementById(
        "navProfiles"
    );

const navHistory =
    document.getElementById(
        "navHistory"
    );

const navSettings =
    document.getElementById(
        "navSettings"
    );


const generateView =
    document.getElementById(
        "generateView"
    );

const profilesView =
    document.getElementById(
        "profilesView"
    );


/* =========================================================
   DOM — GENERATE VIEW
========================================================= */

const profileOptions =
    document.getElementById(
        "profileOptions"
    );

const uploadZone =
    document.getElementById(
        "uploadZone"
    );

const imageInput =
    document.getElementById(
        "imageInput"
    );

const imagePreviewGrid =
    document.getElementById(
        "imagePreviewGrid"
    );

const description =
    document.getElementById(
        "description"
    );

const characterCount =
    document.getElementById(
        "characterCount"
    );

const summaryProfile =
    document.getElementById(
        "summaryProfile"
    );

const summaryVersion =
    document.getElementById(
        "summaryVersion"
    );

const summaryImages =
    document.getElementById(
        "summaryImages"
    );

const summaryCount =
    document.getElementById(
        "summaryCount"
    );

const generateButton =
    document.getElementById(
        "generateButton"
    );


/* =========================================================
   DOM — PROFILE MANAGER
========================================================= */

const newProfileButton =
    document.getElementById(
        "newProfileButton"
    );

const profileSearch =
    document.getElementById(
        "profileSearch"
    );

const profileManagerList =
    document.getElementById(
        "profileManagerList"
    );

const profileEditorEmpty =
    document.getElementById(
        "profileEditorEmpty"
    );

const profileEditorContent =
    document.getElementById(
        "profileEditorContent"
    );

const profileEditorTitle =
    document.getElementById(
        "profileEditorTitle"
    );

const profileStateBadge =
    document.getElementById(
        "profileStateBadge"
    );

const editorVersionBadge =
    document.getElementById(
        "editorVersionBadge"
    );

const loadedVersionBadge =
    document.getElementById(
        "loadedVersionBadge"
    );

const loadedVersionNote =
    document.getElementById(
        "loadedVersionNote"
    );

const profileNameInput =
    document.getElementById(
        "profileNameInput"
    );

const profileDescriptionInput =
    document.getElementById(
        "profileDescriptionInput"
    );

const profileInstructionEditor =
    document.getElementById(
        "profileInstructionEditor"
    );

const instructionCharacterCount =
    document.getElementById(
        "instructionCharacterCount"
    );

const saveDetailsButton =
    document.getElementById(
        "saveDetailsButton"
    );

const saveVersionButton =
    document.getElementById(
        "saveVersionButton"
    );

const archiveProfileButton =
    document.getElementById(
        "archiveProfileButton"
    );

const restoreProfileButton =
    document.getElementById(
        "restoreProfileButton"
    );

const versionHistoryList =
    document.getElementById(
        "versionHistoryList"
    );


/* =========================================================
   DOM — CREATE PROFILE MODAL
========================================================= */

const newProfileModal =
    document.getElementById(
        "newProfileModal"
    );

const modalCloseButton =
    document.getElementById(
        "modalCloseButton"
    );

const cancelCreateProfile =
    document.getElementById(
        "cancelCreateProfile"
    );

const newProfileForm =
    document.getElementById(
        "newProfileForm"
    );

const newProfileName =
    document.getElementById(
        "newProfileName"
    );

const newProfileDescription =
    document.getElementById(
        "newProfileDescription"
    );

const newProfileInstruction =
    document.getElementById(
        "newProfileInstruction"
    );

const newInstructionCharacterCount =
    document.getElementById(
        "newInstructionCharacterCount"
    );

const createProfileButton =
    document.getElementById(
        "createProfileButton"
    );


/* =========================================================
   OTHER
========================================================= */

const toast =
    document.getElementById(
        "toast"
    );


/* =========================================================
   APPLICATION STATE
========================================================= */

let profiles = [];

let managerProfiles = [];

let selectedProfileId = null;

let selectedProfileVersionId = null;

let selectedImages = [];

let selectedCount = "auto";

let editingProfileId = null;

let loadedEditorVersionNumber = null;

let toastTimer = null;


/* =========================================================
   NAVIGATION
========================================================= */

function showView(
    viewName
) {

    generateView.classList.toggle(
        "hidden-view",
        viewName !== "generate"
    );

    profilesView.classList.toggle(
        "hidden-view",
        viewName !== "profiles"
    );


    navGenerate.classList.toggle(
        "active",
        viewName === "generate"
    );

    navProfiles.classList.toggle(
        "active",
        viewName === "profiles"
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


        if (
            editingProfileId === null
        ) {

            const preferredProfile =
                selectedProfileId
                ??
                managerProfiles[0]?.id;


            if (
                preferredProfile
            ) {

                await openProfileEditor(
                    preferredProfile
                );

            }

        }

    }
);


navHistory.addEventListener(
    "click",
    () => {

        showToast(
            "History will be connected when generation jobs are added."
        );

    }
);


navSettings.addEventListener(
    "click",
    () => {

        showToast(
            "Settings will be added when we connect the AI providers."
        );

    }
);


/* =========================================================
   API ERROR HELPER
========================================================= */

async function getApiErrorMessage(
    response
) {

    try {

        const data =
            await response.json();


        if (
            typeof data.detail === "string"
        ) {

            return data.detail;

        }


        if (
            data.detail
        ) {

            return JSON.stringify(
                data.detail
            );

        }

    } catch {
        // Ignore parsing failure.
    }


    return (
        `Request failed with status ${response.status}`
    );

}


/* =========================================================
   LOAD ACTIVE GENERATION PROFILES
========================================================= */

async function loadProfiles(
    preferredProfileId = selectedProfileId
) {

    profileOptions.innerHTML = `
        <div class="profiles-loading">

            <span class="loading-spinner"></span>

            Loading generation profiles...

        </div>
    `;


    try {

        const response =
            await fetch(
                "/api/profiles"
            );


        if (!response.ok) {

            throw new Error(
                await getApiErrorMessage(
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
                ? data.profiles
                : [];


        renderGenerateProfiles(
            preferredProfileId
        );


    } catch (error) {

        console.error(
            error
        );


        profileOptions.innerHTML = `
            <div class="profiles-error">
                Could not load generation profiles.
            </div>
        `;


        selectedProfileId = null;

        selectedProfileVersionId = null;


        summaryProfile.textContent =
            "Unavailable";

        summaryVersion.textContent =
            "—";

    }

}


/* =========================================================
   RENDER GENERATE PROFILES
========================================================= */

function renderGenerateProfiles(
    preferredProfileId
) {

    profileOptions.innerHTML = "";


    if (
        profiles.length === 0
    ) {

        profileOptions.innerHTML = `
            <div class="profiles-empty">
                No active generation profiles.
                Open Profiles to create or restore one.
            </div>
        `;


        selectedProfileId = null;

        selectedProfileVersionId = null;


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


    let profileToSelect =
        profiles.find(
            profile =>
                Number(profile.id)
                ===
                Number(preferredProfileId)
        );


    if (!profileToSelect) {

        profileToSelect =
            profiles[0];

    }


    selectProfile(
        profileToSelect.id
    );

}


/* =========================================================
   GENERATE PROFILE CARD
========================================================= */

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


    const radio =
        document.createElement(
            "input"
        );


    radio.type =
        "radio";

    radio.name =
        "profile";

    radio.value =
        String(
            profile.id
        );


    const icon =
        document.createElement(
            "div"
        );


    icon.className =
        "profile-icon dynamic-profile-icon";


    icon.textContent =
        getProfileInitials(
            profile.name
        );


    const profileText =
        document.createElement(
            "div"
        );


    profileText.className =
        "profile-text";


    const name =
        document.createElement(
            "strong"
        );


    name.textContent =
        profile.name;


    const details =
        document.createElement(
            "span"
        );


    const version =
        `v${profile.version_number}`;


    if (
        profile.description
    ) {

        details.textContent =
            `${version} · ${profile.description}`;

    } else {

        details.textContent =
            version;

    }


    const check =
        document.createElement(
            "div"
        );


    check.className =
        "profile-check";

    check.textContent =
        "✓";


    profileText.appendChild(
        name
    );

    profileText.appendChild(
        details
    );


    card.appendChild(
        radio
    );

    card.appendChild(
        icon
    );

    card.appendChild(
        profileText
    );

    card.appendChild(
        check
    );


    card.addEventListener(
        "click",
        () => {

            selectProfile(
                profile.id
            );

        }
    );


    return card;

}


/* =========================================================
   SELECT GENERATION PROFILE
========================================================= */

function selectProfile(
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
            profile.version_id
        );


    document
        .querySelectorAll(
            ".profile-card"
        )
        .forEach(
            card => {

                const isSelected =
                    Number(
                        card.dataset.profileId
                    )
                    ===
                    selectedProfileId;


                card.classList.toggle(
                    "active-profile",
                    isSelected
                );


                const radio =
                    card.querySelector(
                        'input[type="radio"]'
                    );


                if (radio) {

                    radio.checked =
                        isSelected;

                }

            }
        );


    summaryProfile.textContent =
        profile.name;


    summaryVersion.textContent =
        `v${profile.version_number}`;

}


/* =========================================================
   PROFILE INITIALS
========================================================= */

function getProfileInitials(
    name
) {

    if (!name) {
        return "?";
    }


    const words =
        name
            .trim()
            .split(/\s+/)
            .filter(Boolean);


    if (
        words.length === 0
    ) {

        return "?";

    }


    if (
        words.length === 1
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


/* =========================================================
   LOAD PROFILE MANAGER LIBRARY
========================================================= */

async function loadManagerProfiles() {

    try {

        const response =
            await fetch(
                "/api/profiles?include_archived=true"
            );


        if (!response.ok) {

            throw new Error(
                await getApiErrorMessage(
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
                ? data.profiles
                : [];


        renderManagerProfiles();


    } catch (error) {

        console.error(
            error
        );


        profileManagerList.innerHTML = `
            <div class="manager-empty">
                Could not load profiles.
            </div>
        `;

    }

}


/* =========================================================
   RENDER MANAGER PROFILE LIST
========================================================= */

function renderManagerProfiles() {

    profileManagerList.innerHTML =
        "";


    const searchValue =
        profileSearch.value
            .trim()
            .toLowerCase();


    const filteredProfiles =
        managerProfiles.filter(
            profile => {

                const text = (
                    `${profile.name} ${profile.description || ""}`
                ).toLowerCase();


                return text.includes(
                    searchValue
                );

            }
        );


    if (
        filteredProfiles.length === 0
    ) {

        profileManagerList.innerHTML = `
            <div class="manager-empty">
                No profiles found.
            </div>
        `;

        return;

    }


    filteredProfiles.forEach(
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
                `v${profile.version_number}`;


            titleRow.appendChild(
                title
            );

            titleRow.appendChild(
                version
            );


            const descriptionElement =
                document.createElement(
                    "div"
                );


            descriptionElement.className =
                "manager-profile-description";


            descriptionElement.textContent =
                profile.description
                ||
                "No description";


            const status =
                document.createElement(
                    "span"
                );


            status.className =
                "manager-profile-status";


            if (
                Number(profile.is_active)
                === 1
            ) {

                status.textContent =
                    "Active";

            } else {

                status.textContent =
                    "Archived";

                status.classList.add(
                    "archived"
                );

            }


            button.appendChild(
                titleRow
            );

            button.appendChild(
                descriptionElement
            );

            button.appendChild(
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


/* =========================================================
   OPEN PROFILE EDITOR
========================================================= */

async function openProfileEditor(
    profileId,
    versionNumber = null
) {

    try {

        let url =
            `/api/profiles/${profileId}`;


        if (
            versionNumber !== null
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
                await getApiErrorMessage(
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


        loadedEditorVersionNumber =
            Number(
                profile.version_number
            );


        const managerProfile =
            managerProfiles.find(
                item =>
                    Number(item.id)
                    ===
                    editingProfileId
            );


        const latestVersion =
            managerProfile
                ?
                Number(
                    managerProfile.version_number
                )
                :
                loadedEditorVersionNumber;


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
            profile.system_instruction;


        loadedVersionBadge.textContent =
            `v${loadedEditorVersionNumber}`;


        editorVersionBadge.textContent =
            `Loaded v${loadedEditorVersionNumber} · Latest v${latestVersion}`;


        if (
            loadedEditorVersionNumber
            <
            latestVersion
        ) {

            loadedVersionNote.textContent =
                `You are viewing an older version (v${loadedEditorVersionNumber}). You can edit it and save the result as a new version.`;

        } else {

            loadedVersionNote.textContent =
                "Latest system instruction loaded.";

        }


        updateInstructionCharacterCount();


        const active =
            Number(
                profile.is_active
            )
            ===
            1;


        profileStateBadge.textContent =
            active
                ?
                "Active"
                :
                "Archived";


        profileStateBadge.classList.toggle(
            "active",
            active
        );


        profileStateBadge.classList.toggle(
            "archived",
            !active
        );


        archiveProfileButton.classList.toggle(
            "hidden-element",
            !active
        );


        restoreProfileButton.classList.toggle(
            "hidden-element",
            active
        );


        /*
            Archived profiles remain viewable,
            but must be restored before editing.
        */

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


        renderManagerProfiles();


        await loadVersionHistory(
            editingProfileId
        );


    } catch (error) {

        console.error(
            error
        );


        showToast(
            error.message
        );

    }

}


/* =========================================================
   VERSION HISTORY
========================================================= */

async function loadVersionHistory(
    profileId
) {

    versionHistoryList.innerHTML = `
        <div class="manager-loading">
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
                await getApiErrorMessage(
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


        if (
            versions.length === 0
        ) {

            versionHistoryList.innerHTML = `
                <div class="manager-empty">
                    No versions found.
                </div>
            `;

            return;

        }


        versions.forEach(
            version => {

                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "version-history-item";


                if (
                    Number(
                        version.version_number
                    )
                    ===
                    Number(
                        loadedEditorVersionNumber
                    )
                ) {

                    item.classList.add(
                        "loaded"
                    );

                }


                const main =
                    document.createElement(
                        "div"
                    );


                main.className =
                    "version-history-main";


                const title =
                    document.createElement(
                        "div"
                    );


                title.className =
                    "version-history-title";


                title.textContent =
                    `Version ${version.version_number}`;


                const meta =
                    document.createElement(
                        "div"
                    );


                meta.className =
                    "version-history-meta";


                meta.textContent =
                    `${formatDatabaseDate(version.created_at)} · ${formatNumber(version.character_count)} characters`;


                main.appendChild(
                    title
                );

                main.appendChild(
                    meta
                );


                const loadButton =
                    document.createElement(
                        "button"
                    );


                loadButton.className =
                    "version-load-button";


                loadButton.type =
                    "button";


                loadButton.textContent =
                    (
                        Number(
                            version.version_number
                        )
                        ===
                        Number(
                            loadedEditorVersionNumber
                        )
                    )
                        ?
                        "Loaded"
                        :
                        "Load";


                loadButton.disabled =
                    (
                        Number(
                            version.version_number
                        )
                        ===
                        Number(
                            loadedEditorVersionNumber
                        )
                    );


                loadButton.addEventListener(
                    "click",
                    () => {

                        openProfileEditor(
                            profileId,
                            version.version_number
                        );

                    }
                );


                item.appendChild(
                    main
                );

                item.appendChild(
                    loadButton
                );


                versionHistoryList.appendChild(
                    item
                );

            }
        );


    } catch (error) {

        console.error(
            error
        );


        versionHistoryList.innerHTML = `
            <div class="manager-empty">
                Could not load version history.
            </div>
        `;

    }

}


/* =========================================================
   PROFILE SEARCH
========================================================= */

profileSearch.addEventListener(
    "input",
    () => {

        renderManagerProfiles();

    }
);


/* =========================================================
   SAVE PROFILE DETAILS
========================================================= */

saveDetailsButton.addEventListener(
    "click",
    async () => {

        if (!editingProfileId) {
            return;
        }


        const name =
            profileNameInput.value.trim();


        if (!name) {

            showToast(
                "Profile name cannot be empty."
            );

            return;

        }


        setButtonBusy(
            saveDetailsButton,
            true,
            "Saving..."
        );


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

                        body: JSON.stringify({
                            name:
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
                    await getApiErrorMessage(
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

            console.error(
                error
            );


            showToast(
                error.message
            );


        } finally {

            setButtonBusy(
                saveDetailsButton,
                false,
                "Save Details"
            );

        }

    }
);


/* =========================================================
   SAVE NEW SYSTEM INSTRUCTION VERSION
========================================================= */

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
                "Save this instruction as a new profile version?"
            );


        if (!confirmed) {
            return;
        }


        setButtonBusy(
            saveVersionButton,
            true,
            "Saving New Version..."
        );


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

                        body: JSON.stringify({
                            system_instruction:
                                instruction
                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    await getApiErrorMessage(
                        response
                    )
                );

            }


            const updatedProfile =
                await response.json();


            await loadProfiles(
                editingProfileId
            );


            await loadManagerProfiles();


            await openProfileEditor(
                editingProfileId
            );


            showToast(
                `Version ${updatedProfile.version_number} created successfully.`
            );


        } catch (error) {

            console.error(
                error
            );


            showToast(
                error.message
            );


        } finally {

            setButtonBusy(
                saveVersionButton,
                false,
                "Save as New Version"
            );

        }

    }
);


/* =========================================================
   ARCHIVE PROFILE
========================================================= */

archiveProfileButton.addEventListener(
    "click",
    async () => {

        if (!editingProfileId) {
            return;
        }


        const confirmed =
            window.confirm(
                "Archive this profile? It will disappear from Generate, but its versions will remain saved."
            );


        if (!confirmed) {
            return;
        }


        try {

            const response =
                await fetch(
                    `/api/profiles/${editingProfileId}`,
                    {
                        method:
                            "DELETE"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    await getApiErrorMessage(
                        response
                    )
                );

            }


            await response.json();


            const archivedId =
                editingProfileId;


            await loadProfiles();

            await loadManagerProfiles();

            await openProfileEditor(
                archivedId
            );


            showToast(
                "Profile archived."
            );


        } catch (error) {

            console.error(
                error
            );


            showToast(
                error.message
            );

        }

    }
);


/* =========================================================
   RESTORE PROFILE
========================================================= */

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
                        method:
                            "POST"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    await getApiErrorMessage(
                        response
                    )
                );

            }


            await response.json();


            const restoredId =
                editingProfileId;


            await loadProfiles(
                restoredId
            );

            await loadManagerProfiles();

            await openProfileEditor(
                restoredId
            );


            showToast(
                "Profile restored."
            );


        } catch (error) {

            console.error(
                error
            );


            showToast(
                error.message
            );

        }

    }
);


/* =========================================================
   INSTRUCTION CHARACTER COUNT
========================================================= */

function updateInstructionCharacterCount() {

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
    updateInstructionCharacterCount
);


/* =========================================================
   CREATE PROFILE MODAL
========================================================= */

function openCreateProfileModal() {

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


    setTimeout(
        () => {

            newProfileName.focus();

        },
        50
    );

}


function closeCreateProfileModal() {

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
    openCreateProfileModal
);


modalCloseButton.addEventListener(
    "click",
    closeCreateProfileModal
);


cancelCreateProfile.addEventListener(
    "click",
    closeCreateProfileModal
);


newProfileModal.addEventListener(
    "click",
    event => {

        if (
            event.target
            ===
            newProfileModal
        ) {

            closeCreateProfileModal();

        }

    }
);


document.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Escape"
            &&
            newProfileModal.classList.contains(
                "visible"
            )
        ) {

            closeCreateProfileModal();

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
            `${formatNumber(length)} ${
                length === 1
                    ?
                    "character"
                    :
                    "characters"
            }`;

    }
);


/* =========================================================
   CREATE PROFILE
========================================================= */

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


        if (!name) {

            showToast(
                "Enter a profile name."
            );

            return;

        }


        if (!instruction) {

            showToast(
                "Add a system instruction."
            );

            return;

        }


        setButtonBusy(
            createProfileButton,
            true,
            "Creating..."
        );


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
                                    instruction
                            })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    await getApiErrorMessage(
                        response
                    )
                );

            }


            const createdProfile =
                await response.json();


            closeCreateProfileModal();


            await loadProfiles(
                createdProfile.id
            );


            await loadManagerProfiles();


            await openProfileEditor(
                createdProfile.id
            );


            showToast(
                `${createdProfile.name} created as v1.`
            );


        } catch (error) {

            console.error(
                error
            );


            showToast(
                error.message
            );


        } finally {

            setButtonBusy(
                createProfileButton,
                false,
                "Create Profile"
            );

        }

    }
);


/* =========================================================
   IMAGE UPLOAD
========================================================= */

uploadZone.addEventListener(
    "click",
    () => {

        imageInput.click();

    }
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

    const imageFiles =
        Array.from(
            files
        ).filter(
            file =>
                file.type.startsWith(
                    "image/"
                )
        );


    if (
        imageFiles.length === 0
    ) {

        showToast(
            "Please select image files."
        );

        return;

    }


    for (
        const file
        of imageFiles
    ) {

        if (
            selectedImages.length >= 4
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

}


/* =========================================================
   RENDER REFERENCE IMAGES
========================================================= */

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


            const objectUrl =
                URL.createObjectURL(
                    file
                );


            image.src =
                objectUrl;


            image.alt =
                `Reference ${index + 1}`;


            image.addEventListener(
                "load",
                () => {

                    URL.revokeObjectURL(
                        objectUrl
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


            remove.className =
                "remove-image";


            remove.type =
                "button";


            remove.textContent =
                "×";


            remove.addEventListener(
                "click",
                event => {

                    event.stopPropagation();


                    selectedImages.splice(
                        index,
                        1
                    );


                    renderImages();

                }
            );


            preview.appendChild(
                image
            );

            preview.appendChild(
                number
            );

            preview.appendChild(
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


/* =========================================================
   CREATIVE DIRECTION
========================================================= */

description.addEventListener(
    "input",
    () => {

        const length =
            description.value.length;


        characterCount.textContent =
            `${length} ${
                length === 1
                    ?
                    "character"
                    :
                    "characters"
            }`;

    }
);


/* =========================================================
   OUTPUT COUNT
========================================================= */

const countButtons =
    document.querySelectorAll(
        ".count-button"
    );


countButtons.forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                countButtons.forEach(
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
                    selectedCount === "auto"
                        ?
                        "Auto"
                        :
                        selectedCount;

            }
        );

    }
);


/* =========================================================
   GENERATE BUTTON
========================================================= */

generateButton.addEventListener(
    "click",
    () => {

        if (!selectedProfileId) {

            showToast(
                "Select a generation profile first."
            );

            return;

        }


        if (
            selectedImages.length === 0
        ) {

            showToast(
                "Add at least one reference image first."
            );

            return;

        }


        console.log(
            "Generation data ready:",
            {
                profileId:
                    selectedProfileId,

                profileVersionId:
                    selectedProfileVersionId,

                requestedCount:
                    selectedCount,

                description:
                    description.value.trim(),

                referenceCount:
                    selectedImages.length
            }
        );


        showToast(
            "Profile workflow ready. AI generation connection comes next."
        );

    }
);


/* =========================================================
   GENERIC BUTTON BUSY STATE
========================================================= */

function setButtonBusy(
    button,
    busy,
    text
) {

    button.disabled =
        busy;


    button.textContent =
        text;

}


/* =========================================================
   DATE FORMATTING
========================================================= */

function formatDatabaseDate(
    value
) {

    if (!value) {
        return "Unknown date";
    }


    const normalized =
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


    return date.toLocaleString();

}


/* =========================================================
   NUMBER FORMATTING
========================================================= */

function formatNumber(
    value
) {

    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return value;

    }


    return number.toLocaleString();

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
            3200
        );

}


/* =========================================================
   APPLICATION STARTUP
========================================================= */

async function startApplication() {

    showView(
        "generate"
    );


    await loadProfiles();


    console.log(
        "Image Agent 4C ready."
    );

}


startApplication();