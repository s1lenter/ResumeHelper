document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');

  const closeModal = () => {
      modal.classList.remove('active');
      modalImage.src = '';
  };

  document.querySelectorAll('.resume-about-item img').forEach(img => {
      img.addEventListener('click', () => {
          const fullsizeSrc = img.dataset.fullsize;
          modalImage.src = fullsizeSrc;
          modal.classList.add('active');
      });
  });

  modal.addEventListener('click', closeModal);

  document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && modal.classList.contains('active')) {
          closeModal();
      }
  });
});
