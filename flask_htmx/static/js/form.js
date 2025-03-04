document.addEventListener("DOMContentLoaded", function () {
const fieldConfig = {
    username: { label: "用户名", required: true },
    email: { label: "邮箱", required: true },
    password: { label: "密码", required: true },
};

const validationStates = Object.fromEntries(
    Object.keys(fieldConfig).map((field) => [
    field,
    {
        valid: false,
        message: "",
        touched: false,
    },
    ])
);

window.handleFormSubmit = async function (event) {
    event.preventDefault();

    // 触发所有必填字段验证
    Object.keys(fieldConfig).forEach((field) => {
    if (fieldConfig[field].required) {
        validationStates[field].touched = true;
        const input = document.querySelector(`[name="${field}"]`);
        input.dispatchEvent(new Event("blur"));
    }
    });

    await new Promise((resolve) => setTimeout(resolve, 300));
    updateValidationSummary();

    if (isFormValid()) {
    event.target.submit();
    }
};

function updateValidationSummary() {
    const summaryPanel = document.getElementById("validation-summary");
    const errors = Object.entries(validationStates)
    .filter(
        ([field, state]) =>
        fieldConfig[field].required && (!state.valid || !state.touched)
    )
    .map(([field, state]) => ({
        label: fieldConfig[field].label,
        message: state.valid ? "需要填写" : state.message,
        field: field,
    }));

    if (errors.length > 0) {
    summaryPanel.innerHTML = `
                <h4>需要修正的字段 (${errors.length}):</h4>
                ${errors
                    .map(
                    (e) => `
                    <div class="validation-item" 
                            onclick="scrollToField('${e.field}')">
                        <strong>${e.label}</strong>: ${e.message}
                    </div>
                `
                    )
                    .join("")}
            `;
    summaryPanel.style.display = "block";
    } else {
    summaryPanel.style.display = "none";
    }
}

window.scrollToField = function (field) {
    const input = document.querySelector(`[name="${field}"]`);
    input.scrollIntoView({ behavior: "smooth", block: "center" });
    input.focus();
};

function isFormValid() {
    return Object.entries(fieldConfig).every(
    ([field, config]) =>
        !config.required ||
        (validationStates[field].valid && validationStates[field].touched)
    );
}

function updateValidationState(field, isValid, message) {
    validationStates[field].valid = isValid;
    validationStates[field].message = message;
    document.getElementById("submit-btn").disabled = !isFormValid();
    updateValidationSummary();
}

document.body.addEventListener("htmx:afterSwap", function (evt) {
    const target = evt.detail.target;
    if (target.classList.contains("validation-message")) {
    const field = target.id.replace("-error", "");
    const isValid =
        target.querySelector("[data-valid]")?.dataset.valid === "true";
    const message = target.querySelector(".text-danger")?.textContent || "";
    updateValidationState(field, isValid, message);
    }
});
});
