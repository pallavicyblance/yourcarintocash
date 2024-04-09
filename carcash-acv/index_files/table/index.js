//import Handsontable from "handsontable";
//import "handsontable/dist/handsontable.min.css";
//import "pikaday/css/pikaday.css";

//import { data } from "./constants.js";
//import { progressBarRenderer, starRenderer } from "./customRenderers.js";

/*import {
  alignHeaders,
  addClassesToRows,
  changeCheckboxCell,
  drawCheckboxInRowHeaders
} from "./hooksCallbacks";*/

const example = document.getElementById("handsontable");

var windowHeight = $(window).height();
var topSpace = $("#tab1").offset();
var topOffset = topSpace.top +20;
var tableHeight = windowHeight - topOffset;
console.log('tableHeight', tableHeight);

new Handsontable(example, {
  data,
  height: tableHeight,
  width: '100%',
  //colWidths: [140, 126, 192, 100, 100, 90, 90, 110, 97],
  colHeaders: [
    "Company name",
    "Country",
    "Name",
    "Sell date",
    "Order ID",
    "In stock",
    "Qty",
    "Progress",
    "Rating"
  ],
  columns: [
    { data: 1, type: "text" },
    { data: 2, type: "text" },
    { data: 3, type: "text" },
    {
      data: 4,
      type: "date",
      allowInvalid: false
    },
    { data: 5, type: "text" },
    {
      data: 6,
      type: "checkbox",
      className: "htCenter"
    },
    {
      data: 7,
      type: "numeric"
    },
    {
      data: 8,
      renderer: progressBarRenderer,
      readOnly: true,
      className: "htMiddle"
    },
    {
      data: 9,
      renderer: starRenderer,
      readOnly: true,
      className: "star htCenter"
    }
  ],
  dropdownMenu: true,
  hiddenColumns: {
    indicators: true
  },
  contextMenu: true,
  multiColumnSorting: true,
  filters: true,
  rowHeaders: true,
  manualRowMove: true,
  afterGetColHeader: alignHeaders,
  afterGetRowHeader: drawCheckboxInRowHeaders,
  afterOnCellMouseDown: changeCheckboxCell,
  beforeRenderer: addClassesToRows,
  licenseKey: "non-commercial-and-evaluation"
});
