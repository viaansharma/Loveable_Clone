// SimpleCalculator script

// Define constants for display and calculator buttons
const display = document.getElementById('display');
const buttons = document.querySelectorAll('.calc-button');

/**
 * Append a value to the calculator display.
 * If the display currently shows "0" and the incoming value is not a digit,
 * the function does nothing (prevents leading operators).
 * @param {string} value - The character to append.
 */
function appendToDisplay(value) {
    if (display.value === '0' && /[0-9]/.test(value) === false) return;
    display.value += value;
}

/** Clear the calculator display. */
function clearDisplay() {
    display.value = '';
}

/** Evaluate the expression currently shown in the display. */
function evaluateExpression() {
    try {
        // Using eval for simplicity as per task requirements.
        display.value = eval(display.value).toString();
    } catch {
        display.value = 'Error';
    }
}

// Attach click event listeners to each calculator button.
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const val = button.dataset.value;
        switch (val) {
            case 'C':
                clearDisplay();
                break;
            case '=':
                evaluateExpression();
                break;
            default:
                appendToDisplay(val);
        }
    });
});
