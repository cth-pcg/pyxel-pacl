import { loadPyodide } from "pyodide";

async function main() {
  let pyodide = await loadPyodide();
  console.log(await pyodide.runPythonAsync("1+1"));
};

main();