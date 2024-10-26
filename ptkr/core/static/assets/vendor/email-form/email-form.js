document.querySelector(".email-form").addEventListener("submit", function (event) {
  event.preventDefault(); // Mencegah pengiriman form default

  const formData = new FormData(this);
  document.querySelector(".loading").style.display = 'block'; // Tampilkan loading

  fetch(this.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest' // Agar Django mengenali permintaan AJAX
    },
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Gagal mengirim email'); // Jika tidak OK, lempar error
      }
      return response.json(); // Mengembalikan data JSON
    })
    .then(data => {
      if (data.status === 'success') {
        // Tampilkan pesan sukses dengan alert
        Swal.fire({
          title: (data.message),
          icon: 'success',
          confirmButtonText: 'OK',
          width: '300px',
          height: '250px'
        });
      } else {
        // Jika ada pesan error dari server
        Swal.fire({
          title: (data.message),
          icon: 'danger',
          confirmButtonText: 'OK',
          width: '300px',
          height: '250px'
        });
      }
    })
    .catch(error => {
      Swal.fire({
        title: (error.message),
        icon: 'danger',
        confirmButtonText: 'OK',
        width: '300px',
        height: '250px'
      });
    })
    .finally(() => {
      document.querySelector(".loading").style.display = 'none'; // Sembunyikan loading di akhir
    });
});