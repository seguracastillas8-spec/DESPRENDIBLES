function calcularNuevaCDE() {
  let total = 0;
  document.querySelectorAll(".cartera:checked").forEach(c => {
    total += parseInt(c.dataset.valor);
  });
  document.getElementById("totalCarteras").innerText = total;
}
