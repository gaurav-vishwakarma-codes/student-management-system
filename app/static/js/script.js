// =====================================================
// Custom JS — no external library
// Handles: mobile nav toggle, flash message dismiss,
// "select all" checkbox on the Deleted History page.
// =====================================================

// =====================================================
// LIVE VALIDATION ENGINE
// A JS mirror of the rules in app/services/validations.py,
// so the person sees feedback the instant they type instead
// of only after clicking Search/Add/Update. This is instant
// UI feedback ONLY — the server re-checks everything on
// every submit regardless (see validations.py), since
// client-side JS can always be bypassed or disabled.
//
// Each field has an "add" ruleset (strict — used on Add/
// Update/Register forms) and, where relevant, a "search"
// ruleset (lighter — allows partial text, matching how
// validate_search_query() works server-side).
// =====================================================

var VALID_GENDERS = ["male", "female", "other"];

var VALIDATORS = {

    roll_no: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.indexOf("-") === 0) return "Roll number cannot be negative.";
            if (!/^\d+$/.test(value)) return "Roll number must contain digits only.";
            if (parseInt(value, 10) === 0) return "Roll number must be greater than 0.";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.indexOf("-") === 0) return "Roll Number cannot be negative.";
            if (!/^\d+$/.test(value)) return "Please enter digits only for Roll Number.";
            return null;
        }
    },

    age: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.indexOf("-") === 0) return "Age cannot be negative.";
            if (!/^\d+$/.test(value)) return "Age must contain digits only.";
            var n = parseInt(value, 10);
            if (n < 5 || n > 50) return "Age must be between 5 and 50 years.";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.indexOf("-") === 0) return "Age cannot be negative.";
            if (!/^\d+$/.test(value)) return "Please enter digits only for Age.";
            var n = parseInt(value, 10);
            if (n < 5 || n > 50) return "Age must be between 5 and 50.";
            return null;
        }
    },

    full_name: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z\s]+$/.test(value)) return "Name can contain letters and spaces only.";
            var words = value.split(/\s+/).filter(Boolean);
            if (words.length < 2) return "Please enter first and last name. Example: Rahul Sharma.";
            for (var i = 0; i < words.length; i++) {
                if (words[i].length < 3) return "Each part of the name must contain at least 3 letters.";
            }
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z\s]+$/.test(value)) return "Full Name can contain letters and spaces only.";
            return null;
        }
    },

    gender: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z]+$/.test(value)) return "Gender can contain letters only.";
            if (VALID_GENDERS.indexOf(value.toLowerCase()) === -1) return "Please enter Male, Female, or Other.";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z]+$/.test(value)) return "Please enter letters only for Gender.";
            var typed = value.toLowerCase();
            var isValid = VALID_GENDERS.some(function (g) { return g.indexOf(typed) === 0; });
            if (!isValid) return "Please enter a valid gender: Male, Female, or Other.";
            return null;
        }
    },

    course: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.length < 2) return "Course name must contain at least 2 characters.";
            if (/^\d+$/.test(value)) return "Course name must contain at least one letter.";
            if (!/^[A-Za-z\s.]+$/.test(value)) return "Course name can contain letters, spaces, and dots only.";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z\s.]+$/.test(value)) return "Course can contain letters, spaces, and dots only.";
            return null;
        }
    },

    email: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[\w.-]+@[\w.-]+\.\w+$/.test(value)) return "Please enter a valid email address. Example: abc123@gmail.com";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[\w.@-]+$/.test(value)) return "Email search can contain letters, numbers, and @ . _ - only.";
            return null;
        }
    },

    phone: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.indexOf("-") === 0) return "Phone number cannot be negative.";
            if (!/^\d+$/.test(value)) return "Phone number must contain digits only.";
            if (value.length !== 10) return "Phone number must be exactly 10 digits.";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.indexOf("-") === 0) return "Phone Number cannot be negative.";
            if (!/^\d+$/.test(value)) return "Please enter digits only for Phone.";
            return null;
        }
    },

    address: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (value.length < 2) return "Address must contain at least 2 characters.";
            if (/^\d+$/.test(value)) return "Address must contain letters and cannot be numbers only.";
            return null;
        },
        search: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z0-9\s,./-]+$/.test(value)) return "Address can contain letters, numbers, spaces, and basic punctuation only (no symbols like @, #, or $).";
            return null;
        }
    },

    username: {
        add: function (value) {
            value = value.trim();
            if (value === "") return null;
            if (!/^[A-Za-z0-9_]+$/.test(value)) return "Username can only contain letters, numbers, and underscore (_). Example: admin_1";
            if (/^\d+$/.test(value)) return "Username must contain at least one letter.";
            if (value.length < 3) return "Username must be at least 3 characters long.";
            return null;
        }
    },

    password: {
        add: function (value) {
            if (value === "") return null;
            if (value.length < 8) return "Password must be at least 8 characters long.";
            if (!/[A-Za-z]/.test(value)) return "Password must contain at least one letter (A-Z or a-z).";
            if (!/\d/.test(value)) return "Password must contain at least one number (0-9).";
            if (!/[^A-Za-z0-9]/.test(value)) return "Password must contain at least one special character (@, #, $, %, etc.).";
            return null;
        }
    }

};

// SHOWS/HIDES ONE INPUT'S INLINE ERROR MESSAGE, CREATING
// THE MESSAGE ELEMENT THE FIRST TIME IT'S NEEDED
function runFieldValidation(input, field, mode) {

    var validatorGroup = VALIDATORS[field];
    if (!validatorGroup) return;

    var validatorFn = validatorGroup[mode] || validatorGroup.add;
    if (!validatorFn) return;

    var errorEl = input._liveErrorEl;

    if (!errorEl) {
        errorEl = document.createElement("div");
        errorEl.className = "field-error-msg d-none";
        input.insertAdjacentElement("afterend", errorEl);
        input._liveErrorEl = errorEl;
    }

    var error = validatorFn(input.value);

    if (error) {
        errorEl.textContent = error;
        errorEl.classList.remove("d-none");
        input.classList.add("field-invalid");
    } else {
        errorEl.textContent = "";
        errorEl.classList.add("d-none");
        input.classList.remove("field-invalid");
    }
}

// WIRES UP EVERY [data-validate] INPUT ON THE PAGE — USED FOR
// FIELDS WHOSE TYPE NEVER CHANGES (ADD STUDENT, UPDATE STUDENT
// PER-FIELD FORMS, REGISTER, LOGIN). SEARCH-STYLE PAGES WHERE
// THE FIELD DEPENDS ON A DROPDOWN ARE WIRED SEPARATELY BELOW.
function wireUpStaticLiveValidation() {

    document.querySelectorAll("[data-validate]").forEach(function (input) {

        var field = input.getAttribute("data-validate");
        var mode  = input.getAttribute("data-validate-mode") || "add";

        input.addEventListener("input", function () {
            runFieldValidation(input, field, mode);
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {

    wireUpStaticLiveValidation();

    // ==========================================
    // MOBILE NAV TOGGLE
    // ==========================================

    var toggleBtn = document.getElementById("navToggle");
    var navLinks  = document.getElementById("navLinks");

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener("click", function () {
            navLinks.classList.toggle("open");
        });
    }

    // ==========================================
    // DISMISSABLE FLASH MESSAGES (MANUAL + AUTO)
    // Every flash message (success/error/info) now auto-dismisses
    // on its own after a few seconds if the person doesn't close
    // it themselves — same idea as a "toast" notification. Clicking
    // the × button still works instantly at any time, and cancels
    // the auto-dismiss timer so it doesn't try to remove an
    // already-removed element.
    // ==========================================

    var FLASH_AUTO_DISMISS_MS = 6000; // 6 SECONDS

    document.querySelectorAll(".alert").forEach(function (alertBox) {

        function dismiss() {

            // FADE OUT SMOOTHLY, THEN ACTUALLY REMOVE THE ELEMENT
            // ONCE THE CSS TRANSITION HAS FINISHED (see .alert-fade-out
            // in style.css)
            alertBox.classList.add("alert-fade-out");

            setTimeout(function () {
                alertBox.remove();
            }, 400);
        }

        var autoTimer = setTimeout(dismiss, FLASH_AUTO_DISMISS_MS);

        var closeBtn = alertBox.querySelector(".alert-close");

        if (closeBtn) {
            closeBtn.addEventListener("click", function () {
                clearTimeout(autoTimer); // AVOID A DOUBLE-DISMISS LATER
                dismiss();
            });
        }
    });

    // ==========================================
    // UPDATE STUDENT — FIELD PICKER
    // Shows only the chosen field's update form,
    // instead of all 8 forms stacked at once.
    // ==========================================

    var fieldSelect = document.getElementById("fieldSelect");

    if (fieldSelect) {
        fieldSelect.addEventListener("change", function () {

            // HIDE EVERY FIELD BLOCK FIRST
            document.querySelectorAll(".update-field-block").forEach(function (block) {
                block.classList.add("d-none");
            });

            // SHOW ONLY THE CHOSEN ONE
            var chosen = fieldSelect.value;

            if (chosen) {
                var target = document.getElementById("field-" + chosen);
                if (target) {
                    target.classList.remove("d-none");

                    // FOCUS THE FIRST INPUT FOR CONVENIENCE
                    var firstInput = target.querySelector("input[type='text']");
                    if (firstInput) {
                        firstInput.focus();
                    }
                }
            }
        });
    }

    // ==========================================
    // "SELECT ALL" CHECKBOX — Deleted History page
    // Mirrors the Ctrl+A behaviour from the Tkinter
    // Treeview in gui/view_deleted_history_window.py
    //
    // IMPORTANT: only checks/unchecks rows that are
    // currently VISIBLE. Without this, ticking "select
    // all" while a filter is active would silently
    // select rows hidden by the filter too — which
    // would restore students the user never saw or
    // meant to pick.
    // ==========================================

    var selectAll = document.getElementById("selectAll");

    if (selectAll) {
        selectAll.addEventListener("change", function () {
            document.querySelectorAll(".row-checkbox").forEach(function (cb) {
                var row = cb.closest("tr");
                var isVisible = row && row.style.display !== "none";

                if (isVisible) {
                    cb.checked = selectAll.checked;
                }
            });
        });
    }

    // ==========================================
    // LIVE TABLE FILTER
    // Used on the Deleted History and Updated
    // History pages, which can have 100+ rows.
    // Typing filters visible rows instantly by
    // matching against text — no page reload, so
    // checkbox selections on the Deleted History
    // page are never lost.
    //
    // Also re-applies itself once immediately on
    // page load (not just on typing). This matters
    // when the input arrives PRE-FILLED by the server
    // (e.g. Restore/Permanently Delete redirected back
    // with ?filter_query preserved) — without this, the
    // text would show in the box but the table itself
    // would stay unfiltered until the user typed again.
    //
    // fieldSelectId is OPTIONAL. When given, the person
    // first picks WHICH column to filter by (e.g. "Full
    // Name") from a dropdown, and typing then only matches
    // that specific column — via each <td>'s data-field
    // attribute — instead of the whole row's text. Picking
    // "All Fields" (empty value) checks every column instead.
    // ==========================================

    // FIELDS THAT NEED A "STARTS WITH" MATCH RATHER THAN
    // "CONTAINS ANYWHERE": the word "Male" is literally a
    // substring of "Female" (Fe-MALE), so a plain contains-
    // match on the Gender column — whether it's specifically
    // selected in the dropdown OR reached via "All Fields" —
    // would wrongly count Female rows as matching "Male" too.
    var FILTER_PREFIX_MATCH_FIELDS = ["gender"];

    function cellTextMatches(cellText, term, field) {

        var isPrefixField = FILTER_PREFIX_MATCH_FIELDS.indexOf(field) !== -1;

        return isPrefixField
            ? cellText.indexOf(term) === 0       // STARTS WITH
            : cellText.indexOf(term) !== -1;     // CONTAINS ANYWHERE
    }

    function wireUpTableFilter(inputId, tbodyId, noMatchId, fieldSelectId) {

        var input       = document.getElementById(inputId);
        var tbody       = document.getElementById(tbodyId);
        var noMatch     = noMatchId ? document.getElementById(noMatchId) : null;
        var fieldSelect = fieldSelectId ? document.getElementById(fieldSelectId) : null;

        if (!input || !tbody) {
            return;
        }

        function applyFilter() {

            var term          = input.value.trim().toLowerCase();
            var selectedField = fieldSelect ? fieldSelect.value : "";
            var visibleCount  = 0;

            tbody.querySelectorAll("tr").forEach(function (row) {

                var matches;

                if (term === "") {

                    matches = true;

                } else if (selectedField) {

                    // MATCH ONLY THE CHOSEN COLUMN'S CELL, USING
                    // THAT FIELD'S OWN MATCHING RULE
                    var cell = row.querySelector('[data-field="' + selectedField + '"]');
                    matches = cell
                        ? cellTextMatches(cell.textContent.toLowerCase(), term, selectedField)
                        : false;

                } else {

                    // "ALL FIELDS" — CHECK EVERY CELL, EACH WITH ITS
                    // OWN APPROPRIATE RULE (E.G. GENDER STILL USES
                    // "STARTS WITH" EVEN HERE, SO SEARCHING "MALE"
                    // NEVER PULLS IN FEMALE ROWS)
                    matches = false;

                    row.querySelectorAll("td").forEach(function (cell) {

                        if (matches) {
                            return; // ALREADY MATCHED THIS ROW — SKIP THE REST
                        }

                        var field    = cell.getAttribute("data-field") || "";
                        var cellText = cell.textContent.toLowerCase();

                        if (cellTextMatches(cellText, term, field)) {
                            matches = true;
                        }
                    });
                }

                row.style.display = matches ? "" : "none";

                if (matches) {
                    visibleCount += 1;
                }
            });

            if (noMatch) {
                noMatch.classList.toggle("d-none", visibleCount !== 0);
            }
        }

        input.addEventListener("input", applyFilter);

        if (fieldSelect) {
            // SWITCHING WHICH COLUMN TO FILTER BY STARTS
            // THE SEARCH TEXT FRESH, SAME REASONING AS THE
            // SEARCH/UPDATE PAGES' FIELD DROPDOWNS
            fieldSelect.addEventListener("change", function () {
                input.value = "";
                applyFilter();
            });
        }

        // RUN ONCE IMMEDIATELY IN CASE THE SERVER ALREADY
        // PRE-FILLED THIS INPUT WITH A PREVIOUS FILTER TEXT
        applyFilter();
    }

    wireUpTableFilter("deletedSearchInput", "deletedTableBody", "deletedNoMatch", "deletedFilterField");
    wireUpTableFilter("updatedSearchInput", "updatedTableBody", "updatedNoMatch", "updatedFilterField");
    wireUpTableFilter("studentsSearchInput", "studentsTableBody", "studentsNoMatch", "studentsFilterField");

    // ==========================================
    // SELECTION-COUNT BUTTON LABELS
    // Any button with data-label-zero / data-label-one /
    // data-label-many automatically swaps its visible text
    // based on how many ".row-checkbox" boxes are ticked in
    // its enclosing <form> — 0 / 1 / many wording, e.g.
    // "Delete Selected" -> "Delete Selected Student" ->
    // "Delete 3 Selected Students". Mirrors the singular/
    // plural Restore-button behaviour from the original
    // Tkinter Treeview (update_restore_btn_label).
    //
    // SELECTION-AWARE CONFIRMATION
    // A button can also carry data-confirm="...". That
    // confirm() popup is only shown if at least one row is
    // actually ticked. With nothing selected, the click is
    // allowed straight through so the server's own "please
    // select at least one" error shows immediately — instead
    // of asking the user to confirm an action that was going
    // to fail anyway.
    // ==========================================

    document.querySelectorAll("[data-label-zero]").forEach(function (btn) {

        var form = btn.closest("form");

        if (!form) {
            return;
        }

        function getCheckedCount() {
            return form.querySelectorAll(".row-checkbox:checked").length;
        }

        function updateLabel() {

            var checkedCount = getCheckedCount();

            if (checkedCount === 0) {
                btn.textContent = btn.getAttribute("data-label-zero");
            } else if (checkedCount === 1) {
                btn.textContent = btn.getAttribute("data-label-one");
            } else {
                btn.textContent = btn.getAttribute("data-label-many").replace("{n}", checkedCount);
            }
        }

        form.addEventListener("change", function (event) {
            if (event.target.classList.contains("row-checkbox") || event.target.id === "selectAll") {
                updateLabel();
            }
        });

        // ONLY ASK FOR CONFIRMATION WHEN SOMETHING IS ACTUALLY SELECTED
        var confirmMessage = btn.getAttribute("data-confirm");

        if (confirmMessage) {
            btn.addEventListener("click", function (event) {

                if (getCheckedCount() === 0) {
                    // NOTHING SELECTED — LET IT SUBMIT SO THE SERVER'S
                    // OWN VALIDATION MESSAGE SHOWS, SKIP THE POPUP
                    return;
                }

                if (!confirm(confirmMessage)) {
                    event.preventDefault();
                }
            });
        }

        // SET THE CORRECT INITIAL LABEL ON PAGE LOAD TOO
        updateLabel();
    });

    // ==========================================
    // SEARCH FIELD DROPDOWN — PLACEHOLDER TEXT +
    // CLEAR STALE RESULTS
    // Used on the Search page and the Delete page
    // (both use the same "pick a field, type a
    // value" pattern). Two things happen the moment
    // the dropdown changes:
    //   1. The placeholder updates to describe what
    //      that field expects (e.g. "Age (5-50)"),
    //      instead of a generic "Enter value".
    //   2. Any results still showing from the PREVIOUS
    //      field's search are hidden — otherwise
    //      switching from "Full Name" to "Age" clears
    //      the text box but leaves old Full-Name
    //      results sitting on screen looking current.
    // ==========================================

    var SEARCH_FIELD_PLACEHOLDERS = {
        "roll_no":   "Enter Roll Number (digits only)",
        "full_name": "Enter Full Name (letters only)",
        "age":       "Enter Age (must be between 5 and 50)",
        "gender":    "Enter Gender: Male, Female, or Other",
        "course":    "Enter Course, e.g. BCA or B.Sc",
        "email":     "Enter Email or part of it",
        "phone":     "Enter Phone Number (digits only)",
        "address":   "Enter Address"
    };

    function wireUpSearchFieldReset(selectId, inputId, resultsWrapId) {

        var select      = document.getElementById(selectId);
        var input       = document.getElementById(inputId);
        var resultsWrap = resultsWrapId ? document.getElementById(resultsWrapId) : null;

        if (!select || !input) {
            return;
        }

        function applyPlaceholder() {
            input.placeholder = SEARCH_FIELD_PLACEHOLDERS[select.value] || "Enter value to search";
        }

        // LIVE VALIDATION FOR THIS INPUT — RE-EVALUATED AGAINST
        // WHICHEVER FIELD IS CURRENTLY SELECTED, SINCE THE SAME
        // TEXT BOX SERVES A DIFFERENT FIELD DEPENDING ON THE
        // DROPDOWN (E.G. THE SAME BOX VALIDATES AS "AGE" OR AS
        // "GENDER" DEPENDING ON WHAT'S PICKED)
        function runValidationForCurrentField() {
            if (select.value) {
                runFieldValidation(input, select.value, "search");
            }
        }

        input.addEventListener("input", runValidationForCurrentField);

        select.addEventListener("change", function () {

            input.value = "";
            applyPlaceholder();

            // CLEAR ANY ERROR LEFT OVER FROM THE PREVIOUS FIELD
            if (input._liveErrorEl) {
                input._liveErrorEl.classList.add("d-none");
                input.classList.remove("field-invalid");
            }

            if (resultsWrap) {
                resultsWrap.innerHTML = "";
            }
        });

        // SET THE CORRECT PLACEHOLDER FOR WHATEVER FIELD IS
        // ALREADY SELECTED WHEN THE PAGE LOADS (E.G. AFTER A
        // SEARCH, THE SERVER RE-RENDERS WITH THAT FIELD STILL
        // CHOSEN)
        applyPlaceholder();

        // ALSO VALIDATE IMMEDIATELY IN CASE THE SERVER RE-RENDERED
        // THE PAGE WITH A QUERY ALREADY TYPED IN (E.G. AFTER A
        // FAILED SEARCH)
        runValidationForCurrentField();
    }

    wireUpSearchFieldReset("searchByDropdown", "searchQueryInput", "searchResultsWrap");
    wireUpSearchFieldReset("deleteSearchByDropdown", "deleteSearchQueryInput", "deleteResultsWrap");

    // ==========================================
    // PASSWORD SHOW/HIDE TOGGLE (REGISTER PAGE)
    // Matches the eye-icon behaviour from the original
    // Tkinter register_window.py — click to reveal the
    // typed password, click again to hide it.
    // ==========================================

    var passwordInput  = document.getElementById("registerPasswordInput");
    var passwordToggle = document.getElementById("registerPasswordToggle");

    if (passwordInput && passwordToggle) {
        passwordToggle.addEventListener("click", function () {

            var isHidden = passwordInput.type === "password";

            passwordInput.type = isHidden ? "text" : "password";
            passwordToggle.textContent = isHidden ? "🙈" : "👁";
            passwordToggle.title = isHidden ? "Hide password" : "Show password";
        });
    }

});