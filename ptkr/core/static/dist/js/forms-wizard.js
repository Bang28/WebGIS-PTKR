$(document).ready(function () {
    var current_fs, next_fs, previous_fs; // fieldsets
    var opacity;
    var current = 1;
    var steps = $("fieldset").length;

    setProgressBar(current);

    // Fungsi validasi
    function validateForm(current_fs) {
        const requiredInputs = current_fs.find('[required]');
        let valid = true;

        requiredInputs.each(function () {
            // Menghapus pesan error sebelumnya (jika ada)
            $(this).next('small.error-message').remove();
            
            // Debugging untuk melihat nilai input
            if (!$(this).val()) {
                valid = false;
                $(this).addClass('error'); // Menambahkan kelas error
                
                // Menambahkan pesan error di bawah input
                $(this).after('<small class="error-message" style="color: red; display: block;">* Kolom ini wajib diisi.</small>');
            } else {
                $(this).removeClass('error'); // Menghapus kelas error
            }

            // Validasi untuk input type number
            if ($(this).attr('type') === 'number') {
                var value = $(this).val();
                // Menggunakan regex untuk memeriksa apakah input adalah angka
                if (value === '' || isNaN(value) || !/^\d*\.?\d+$/.test(value)) {
                    valid = false;
                    $(this).addClass('error'); // Menambahkan kelas error
                } else {
                    $(this).removeClass('error'); // Menghapus kelas error
                }
            }
        });
        return valid; // Kembalikan status validasi
    }

    $(".next").click(function () {
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        // Validasi saat klik Next
        if (!validateForm(current_fs)) {
            var Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 5000,
                timerProgressBar: true,
            });

            Toast.fire({
                icon: 'warning',
                title: 'Kolom Kosong/Belum Di ISI',
                text: 'Terdapat kolom yang tidak boleh kosong, silahkan kembali ke Step sebelumnya!'
            });
            // return; // Jangan lanjutkan jika validasi gagal
        }

        // Tampilkan fieldset berikutnya
        next_fs.show();
        // Sembunyikan fieldset saat ini dengan style
        current_fs.animate({ opacity: 0 }, {
            step: function (now) {
                // Untuk membuat animasi tampilan fieldset
                opacity = 1 - now;
                current_fs.css({ 'display': 'none', 'position': 'relative' });
                next_fs.css({ 'opacity': opacity });
            },
            duration: 500
        });
        setProgressBar(++current);
    });

    $(".previous").click(function () {
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        // Tampilkan fieldset sebelumnya
        previous_fs.show();

        // Sembunyikan fieldset saat ini dengan style
        current_fs.animate({ opacity: 0 }, {
            step: function (now) {
                // Untuk membuat animasi tampilan fieldset
                opacity = 1 - now;
                current_fs.css({ 'display': 'none', 'position': 'relative' });
                previous_fs.css({ 'opacity': opacity });
            },
            duration: 500
        });
        setProgressBar(--current);
    });

    function setProgressBar(curStep) {
        var percent = parseFloat(100 / steps) * curStep;
        percent = percent.toFixed();
        $(".progress-bar").css("width", percent + "%");
    }

    $(".submit").click(function () {
        return false;
    });

    // Tambahkan event listener untuk validasi real-time pada input bertipe number
    $('input[type="number"]').on('input', function () {
        var value = $(this).val();
        var valid = true;

        // Clear previous errors
        $(this).removeClass('error');

        // Memeriksa apakah input adalah angka
        if (value === '' || isNaN(value) || !/^\d*\.?\d+$/.test(value)) {
            valid = false;
            var Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 5000,
                timerProgressBar: true,
            });

            Toast.fire({
                icon: 'warning',
                title: 'Input Salah',
                text: 'Input berupa angka dan gunakan titik (.) sebagai pemisah angka / pengganti koma!'
            });
            $(this).addClass('error');
        }
    });
});
