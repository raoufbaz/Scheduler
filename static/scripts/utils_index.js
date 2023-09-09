// reset program_id value when program_title is reset.
programInput.addEventListener("input", function (event) {
  if (programInput.value === "") {
    programId.value = "";
  }
});
