document.addEventListener('DOMContentLoaded', function () {
  const allowedTextareaLength = 500;

  const smiles = document.querySelectorAll('.review-content .smile');
  const hiddenInput = document.querySelector('input[name=emotion]');
  const counter = document.querySelector('.review-content__counter');
  const textarea = document.querySelector('.review-content textarea');

  smiles.forEach((e) => e.addEventListener('click', function () {
      hiddenInput.value = this.getAttribute('data-value');
      smiles.forEach((e) => e.classList.remove('active'));
      this.classList.add('active');
    })
  );

  textarea.addEventListener('keyup', function () {
    if (this.value.length <= allowedTextareaLength) {
      counter.textContent = this.value.length + '/' + allowedTextareaLength;
    } else {
      this.value = this.value.substring(0, allowedTextareaLength);
      counter.textContent = allowedTextareaLength + '/' + allowedTextareaLength;
    }
  });
});
