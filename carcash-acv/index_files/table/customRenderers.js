//import Handsontable from "handsontable";

const addClassWhenNeeded = (td, cellProperties) => {
  const className = cellProperties.className;

  if (className !== void 0) {
    Handsontable.dom.addClass(td, className);
  }
};

 function progressBarRenderer(
  instance,
  td,
  row,
  column,
  prop,
  value,
  cellProperties
) {
  const div = document.createElement("div");

  div.style.width = `${value * 10}px`;

  addClassWhenNeeded(td, cellProperties);
  Handsontable.dom.addClass(div, "progressBar");
  Handsontable.dom.empty(td);

  td.appendChild(div);
}

 function starRenderer(
  instance,
  td,
  row,
  column,
  prop,
  value,
  cellProperties
) {
  Handsontable.renderers.TextRenderer.apply(this, [
    instance,
    td,
    row,
    column,
    prop,
    "★".repeat(value),
    cellProperties
  ]);
}
