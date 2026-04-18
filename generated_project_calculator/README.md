# SimpleCalculator

A lightweight web‑based calculator built with plain **HTML**, **CSS**, and **JavaScript**. It provides a clean UI for basic arithmetic operations without any external libraries or build steps.

---

## Technology Stack
- **HTML** – Markup for the calculator layout.
- **CSS** – Styling and responsive design.
- **JavaScript** – Core logic encapsulated in a `Calculator` class.

---

## Installation
1. **Clone the repository**
   ```bash
   git clone <repository‑url>
   cd <repo‑folder>
   ```
2. **Open the app**
   - Double‑click `index.html` or open it in any modern browser (Chrome, Firefox, Edge, Safari).
   - No additional tools (npm, webpack, etc.) are required.

---

## Usage
The UI consists of a display area and a grid of buttons.

| Section | Description |
|---------|-------------|
| **Display** | Shows the current expression and the result after evaluation. |
| **Number Buttons (0‑9)** | Click to append digits to the current expression. |
| **Operator Buttons (+, -, *, /, .)** | Append the corresponding operator or decimal point. |
| **Clear (C)** | Clears the entire expression and resets the display. |
| **Equals (=)** | Evaluates the expression and shows the result. |

**Steps**
1. Click numbers and operators to build an arithmetic expression (e.g., `12 + 7 / 3`).
2. Press **C** to start over at any time.
3. Press **=** to calculate the result. The result replaces the expression in the display.

---

## File Structure
- **`index.html`** – Contains the structural markup for the calculator, including the display `<input>` and all calculator buttons.
- **`style.css`** – Provides the visual styling, layout (CSS Grid), and responsive behavior.
- **`script.js`** – Implements the `Calculator` class that handles input, clearing, and evaluation, and wires the DOM events to the UI.
- **`README.md`** – This documentation file.
- **`screenshot.png`** – Placeholder image showing the calculator UI (replace with an actual screenshot).

---

## Future Improvements
- **Keyboard Support** – Allow typing numbers and operators directly from the keyboard.
- **Expression Validation** – Prevent invalid sequences (e.g., two operators in a row) before evaluation.
- **Theming** – Add dark/light mode toggles using CSS variables.
- **Extended Operations** – Include parentheses, exponentiation, and scientific functions.

---

![Calculator Screenshot](screenshot.png)
