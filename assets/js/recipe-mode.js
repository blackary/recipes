(function () {
  const mode = document.querySelector("[data-cook-mode]");
  const start = document.querySelector("[data-start-cooking]");
  const sourceIngredients = document.querySelectorAll("[data-recipe-ingredients] li");
  const sourceSteps = Array.from(document.querySelectorAll("[data-recipe-instructions] li"));

  if (!mode || !start || !sourceSteps.length) return;

  const ingredientList = mode.querySelector("[data-cook-ingredients]");
  const ingredientPanel = mode.querySelector(".cook-ingredients");
  const ingredientToggle = mode.querySelector("[data-cook-ingredients-toggle]");
  const instructionList = mode.querySelector("[data-cook-instructions]");
  const close = mode.querySelector("[data-cook-close]");
  let returnFocus;

  sourceIngredients.forEach((ingredient, index) => {
    const label = document.createElement("label");
    label.className = "cook-ingredient";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.setAttribute("aria-label", `Mark ingredient ${index + 1} complete`);
    const text = document.createElement("span");
    text.textContent = ingredient.textContent.trim();
    label.append(checkbox, text);
    ingredientList.append(label);
  });

  sourceSteps.forEach((step) => {
    const item = document.createElement("li");
    item.textContent = step.textContent.trim();
    instructionList.append(item);
  });

  function openMode() {
    returnFocus = document.activeElement;
    mode.hidden = false;
    document.body.classList.add("cook-mode-open");
    close.focus();
  }

  function closeMode() {
    mode.hidden = true;
    document.body.classList.remove("cook-mode-open");
    ingredientPanel.classList.remove("ingredients-expanded");
    ingredientToggle.setAttribute("aria-expanded", "false");
    ingredientToggle.innerHTML = 'Show all <span aria-hidden="true">↓</span>';
    if (returnFocus) returnFocus.focus();
  }

  start.addEventListener("click", openMode);
  close.addEventListener("click", closeMode);
  ingredientToggle.addEventListener("click", () => {
    const expanded = ingredientPanel.classList.toggle("ingredients-expanded");
    ingredientToggle.setAttribute("aria-expanded", String(expanded));
    ingredientToggle.innerHTML = expanded
      ? 'Collapse <span aria-hidden="true">↑</span>'
      : 'Show all <span aria-hidden="true">↓</span>';
  });
  document.addEventListener("keydown", (event) => {
    if (mode.hidden) return;
    if (event.key === "Escape") closeMode();
  });
})();
