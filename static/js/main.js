function updateSerialNumbers() {
  const tables = ["pending-task-body", "completed-task-body"];
  tables.forEach((id) => {
    const rows = document.querySelectorAll(`#${id} tr`);
    rows.forEach((row, index) => {
      const serial = row.querySelector(".serial-cell");
      if (serial) {
        serial.textContent = index + 1;
      }
    });
  });
}

document.getElementById("add-task-form")?.addEventListener("submit", async function (e) {
  e.preventDefault();
  const formData = new FormData(this);

  const res = await fetch("/", {
    method: "POST",
    body: formData,
    headers: { "X-Requested-With": "XMLHttpRequest" }
  });

  if (res.ok) {
    const html = await res.text();
    const wrapper = document.createElement("tbody");
    wrapper.innerHTML = html;
    const newRow = wrapper.querySelector("tr");

    document.getElementById("pending-task-body")?.appendChild(newRow);
    this.reset();
    updateSerialNumbers();
  }
});

document.addEventListener("click", async function (e) {
  // DELETE
  if (e.target.matches(".btn-delete")) {
    e.preventDefault();
    const id = e.target.getAttribute("data-id");

    const res = await fetch(`/delete/${id}`, { method: "DELETE" });

    if (res.ok) {
      e.target.closest("tr")?.remove();
      updateSerialNumbers();
    }
  }

  // TOGGLE
  if (e.target.matches(".btn-toggle")) {
    e.preventDefault();
    const id = e.target.getAttribute("data-id");

    const res = await fetch(`/toggle/${id}`, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" }
    });

    if (res.ok) {
      const html = await res.text();
      const wrapper = document.createElement("tbody");
      wrapper.innerHTML = html;
      const newRow = wrapper.querySelector("tr");

      const oldRow = document.querySelector(`tr[data-id="${id}"]`);
      oldRow?.remove();

      const status = newRow.dataset.status;
      const targetBody = document.getElementById(
        status === "Completed" ? "completed-task-body" : "pending-task-body"
      );

      targetBody?.appendChild(newRow);
      updateSerialNumbers();
    }
  }
});
