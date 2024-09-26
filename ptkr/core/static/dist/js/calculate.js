// Kalkulator Struktur Atap
function calcAtap() {
    function calculateAreaAtap(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }

    // Ambil nilai input
    var p_sisi_a = parseFloat(document.getElementById("panjang_atap_sisi_a").value) || 0;
    var l_sisi_a = parseFloat(document.getElementById("lebar_atap_sisi_a").value) || 0;
    var p_sisi_b = parseFloat(document.getElementById("panjang_atap_sisi_b").value) || 0;
    var l_sisi_b = parseFloat(document.getElementById("lebar_atap_sisi_b").value) || 0;
    var p_atap_rusak = parseFloat(document.getElementById("panjang_atap_rusak").value) || 0;
    var l_atap_rusak = parseFloat(document.getElementById("lebar_atap_rusak").value) || 0;

    var atap_rsr = parseFloat(document.getElementById("atap_rsr").value) || 0;
    var atap_rr = parseFloat(document.getElementById("atap_rr").value) || 0;
    var atap_rs = parseFloat(document.getElementById("atap_rs").value) || 0;
    var atap_rb = parseFloat(document.getElementById("atap_rb").value) || 0;
    var atap_rsb = parseFloat(document.getElementById("atap_rsb").value) || 0;
    var atap_kts = parseFloat(document.getElementById("atap_kts").value) || 0;

    // Hitung luas
    var luas_a = calculateAreaAtap(p_sisi_a, l_sisi_a);
    var luas_b = calculateAreaAtap(p_sisi_b, l_sisi_b);
    var luas_atap_rusak = calculateAreaAtap(p_atap_rusak, l_atap_rusak);
    // Hitung luas bidang tidak rusak
    var atap_tr = 100 - (atap_rsr + atap_rr + atap_rs + atap_rb + atap_rsb + atap_kts)

    // Update input luas
    document.getElementById("luas_atap_sisi_a").value = luas_a;
    document.getElementById("luas_atap_sisi_b").value = luas_b;
    document.getElementById("luas_atap_rusak").value = luas_atap_rusak;
    document.getElementById("atap_tr").value = atap_tr;

    // Hitung persentase kerusakan (Luas Bidang Rusak / (Luas A + Luas B) * 100%)
    var total_luas_atap = luas_a + luas_b;
    var kerusakan_atap = total_luas_atap ? (luas_atap_rusak / total_luas_atap) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_atap").value = kerusakan_atap.toFixed(2);
}

// Kalkulator Arsitekur Dinding
function calcDinding() {
    function calculateAreaDinding(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }
    function calculateAreaPintuJendela(panjang, lebar, jumlah) {
        return panjang && lebar && jumlah ? panjang * lebar * jumlah : 0;
    }

    // Ambil nilai input
    var p_dinding = parseFloat(document.getElementById("panjang_dinding").value) || 0;
    var t_dinding = parseFloat(document.getElementById("tinggi_dinding").value) || 0;
    var l_pintu = parseFloat(document.getElementById("lebar_pintu").value) || 0;
    var t_pintu = parseFloat(document.getElementById("tinggi_pintu").value) || 0;
    var j_pintu = parseFloat(document.getElementById("jumlah_pintu").value) || 0;
    var l_jendela = parseFloat(document.getElementById("lebar_jendela").value) || 0;
    var t_jendela = parseFloat(document.getElementById("tinggi_jendela").value) || 0;
    var j_jendela = parseFloat(document.getElementById("jumlah_jendela").value) || 0;
    var p_dinding_rusak = parseFloat(document.getElementById("panjang_dinding_rusak").value) || 0;
    var l_dindng_rusak = parseFloat(document.getElementById("lebar_dinding_rusak").value) || 0;

    var dinding_rsr = parseFloat(document.getElementById("dinding_rsr").value) || 0;
    var dinding_rr = parseFloat(document.getElementById("dinding_rr").value) || 0;
    var dinding_rs = parseFloat(document.getElementById("dinding_rs").value) || 0;
    var dinding_rb = parseFloat(document.getElementById("dinding_rb").value) || 0;
    var dinding_rsb = parseFloat(document.getElementById("dinding_rsb").value) || 0;
    var dinding_kts = parseFloat(document.getElementById("dinding_kts").value) || 0;

    // Hitung luas
    var luas_dinding = calculateAreaDinding(p_dinding, t_dinding);
    var luas_pintu = calculateAreaPintuJendela(l_pintu, t_pintu, j_pintu);
    var luas_jendela = calculateAreaPintuJendela(l_jendela, t_jendela, j_jendela);
    var luas_dinding_rusak = calculateAreaDinding(p_dinding_rusak, l_dindng_rusak);

    // Hitung luas bidang tidak rusak
    var dinding_tr = 100 - (dinding_rsr + dinding_rr + dinding_rs + dinding_rb + dinding_rsb + dinding_kts)

    // Update input luas
    document.getElementById("luas_dinding").value = luas_dinding.toFixed(2);
    document.getElementById("luas_pintu").value = luas_pintu.toFixed(2);
    document.getElementById("luas_jendela").value = luas_jendela.toFixed(2);
    document.getElementById("luas_dinding_rusak").value = luas_dinding_rusak.toFixed(2);
    document.getElementById("dinding_tr").value = dinding_tr;

    // Hitung persentase kerusakan (Luas Bidang Rusak / (Luas Dinding - Luas Pintu - Luas Jendela) * 100%)
    var total_luas_dinding = luas_dinding - (luas_pintu + luas_jendela);
    var kerusakan_dinding = total_luas_dinding ? (luas_dinding_rusak / total_luas_dinding) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_dinding").value = kerusakan_dinding.toFixed(2);
}

// Kalkulator Arsitektur Plafon
function calcPlafon() {
    function calculateAreaPlafon(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }

    // Ambil nilai input
    var p_plafon = parseFloat(document.getElementById("panjang_plafon").value) || 0;
    var l_plafon = parseFloat(document.getElementById("lebar_plafon").value) || 0;
    var p_plafon_rusak = parseFloat(document.getElementById("panjang_plafon_rusak").value) || 0;
    var l_plafon_rusak = parseFloat(document.getElementById("lebar_plafon_rusak").value) || 0;

    var plafon_rsr = parseFloat(document.getElementById("plafon_rsr").value) || 0;
    var plafon_rr = parseFloat(document.getElementById("plafon_rr").value) || 0;
    var plafon_rs = parseFloat(document.getElementById("plafon_rs").value) || 0;
    var plafon_rb = parseFloat(document.getElementById("plafon_rb").value) || 0;
    var plafon_rsb = parseFloat(document.getElementById("plafon_rsb").value) || 0;
    var plafon_kts = parseFloat(document.getElementById("plafon_kts").value) || 0;

    // Hitung luas
    var luas_plafon = calculateAreaPlafon(p_plafon, l_plafon);
    var luas_plafon_rusak = calculateAreaPlafon(p_plafon_rusak, l_plafon_rusak);

    // Hitung luas bidang tidak rusak
    var plafon_tr = 100 - (plafon_rsr + plafon_rr + plafon_rs + plafon_rb + plafon_rsb + plafon_kts)

    // Update input luas
    document.getElementById("luas_plafon").value = luas_plafon;
    document.getElementById("luas_plafon_rusak").value = luas_plafon_rusak.toFixed(2);
    document.getElementById("plafon_tr").value = plafon_tr;

    // Hitung persentase kerusakan (Luas Bidang Rusak / Luas Plafon * 100%)
    var kerusakan_plafon = luas_plafon ? (luas_plafon_rusak / luas_plafon) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_plafon").value = kerusakan_plafon.toFixed(2);
}

// Kalkulator Arsitektur Lantai
function calcLantai() {
    function calculateAreaLantai(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }

    // Ambil nilai input
    var p_Lantai = parseFloat(document.getElementById("panjang_lantai").value) || 0;
    var l_Lantai = parseFloat(document.getElementById("lebar_lantai").value) || 0;
    var p_Lantai_rusak = parseFloat(document.getElementById("panjang_lantai_rusak").value) || 0;
    var l_Lantai_rusak = parseFloat(document.getElementById("lebar_lantai_rusak").value) || 0;

    var lantai_rsr = parseFloat(document.getElementById("lantai_rsr").value) || 0;
    var lantai_rr = parseFloat(document.getElementById("lantai_rr").value) || 0;
    var lantai_rs = parseFloat(document.getElementById("lantai_rs").value) || 0;
    var lantai_rb = parseFloat(document.getElementById("lantai_rb").value) || 0;
    var lantai_rsb = parseFloat(document.getElementById("lantai_rsb").value) || 0;
    var lantai_kts = parseFloat(document.getElementById("lantai_kts").value) || 0;

    // Hitung luas
    var luas_lantai = calculateAreaLantai(p_Lantai, l_Lantai);
    var luas_lantai_rusak = calculateAreaLantai(p_Lantai_rusak, l_Lantai_rusak);

    // Hitung luas bidang tidak rusak
    var lantai_tr = 100 - (lantai_rsr + lantai_rr + lantai_rs + lantai_rb + lantai_rsb + lantai_kts)

    // Update input luas
    document.getElementById("luas_Lantai").value = luas_lantai;
    document.getElementById("luas_lantai_rusak").value = luas_lantai_rusak.toFixed(2);
    document.getElementById("lantai_tr").value = lantai_tr;

    // Hitung persentase kerusakan (Luas Bidang Rusak / Luas Lantai * 100%)
    var kerusakan_Lantai = luas_lantai ? (luas_lantai_rusak / luas_lantai) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_lantai").value = kerusakan_Lantai.toFixed(2);
}

// Kalkulator Finishing Plafon
function calcFPlafon() {
    function calculateAreaPlafon(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }

    // Ambil nilai input
    var p_fplafon = parseFloat(document.getElementById("panjang_fplafon").value) || 0;
    var l_fplafon = parseFloat(document.getElementById("lebar_fplafon").value) || 0;
    var p_fplafon_rusak = parseFloat(document.getElementById("panjang_fplafon_rusak").value) || 0;
    var l_fplafon_rusak = parseFloat(document.getElementById("lebar_fplafon_rusak").value) || 0;

    var fplafon_rsr = parseFloat(document.getElementById("fplafon_rsr").value) || 0;
    var fplafon_rr = parseFloat(document.getElementById("fplafon_rr").value) || 0;
    var fplafon_rs = parseFloat(document.getElementById("fplafon_rs").value) || 0;
    var fplafon_rb = parseFloat(document.getElementById("fplafon_rb").value) || 0;
    var fplafon_rsb = parseFloat(document.getElementById("fplafon_rsb").value) || 0;
    var fplafon_kts = parseFloat(document.getElementById("fplafon_kts").value) || 0;

    // Hitung luas
    var luas_fplafon = calculateAreaPlafon(p_fplafon, l_fplafon);
    var luas_fplafon_rusak = calculateAreaPlafon(p_fplafon_rusak, l_fplafon_rusak);

    // Hitung luas bidang tidak rusak
    var fplafon_tr = 100 - (fplafon_rsr + fplafon_rr + fplafon_rs + fplafon_rb + fplafon_rsb + fplafon_kts)

    // Update input luas
    document.getElementById("luas_fplafon").value = luas_fplafon;
    document.getElementById("luas_fplafon_rusak").value = luas_fplafon_rusak.toFixed(2);
    document.getElementById("fplafon_tr").value = fplafon_tr;

    // Hitung persentase kerusakan (Luas Bidang Rusak / Luas Plafon * 100%)
    var kerusakan_fplafon = luas_fplafon ? (luas_fplafon_rusak / luas_fplafon) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_fplafon").value = kerusakan_fplafon.toFixed(2);
}

// Kalkulator Finishing Dinding
function calcFDinding() {
    function calculateAreaDinding(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }
    function calculateAreaPintuJendela(panjang, lebar, jumlah) {
        return panjang && lebar && jumlah ? panjang * lebar * jumlah : 0;
    }

    // Ambil nilai input
    var p_fdinding = parseFloat(document.getElementById("panjang_fdinding").value) || 0;
    var t_fdinding = parseFloat(document.getElementById("tinggi_fdinding").value) || 0;
    var fd_l_pintu = parseFloat(document.getElementById("fd_lebar_pintu").value) || 0;
    var fd_t_pintu = parseFloat(document.getElementById("fd_tinggi_pintu").value) || 0;
    var fd_j_pintu = parseFloat(document.getElementById("fd_jumlah_pintu").value) || 0;
    var fd_l_jendela = parseFloat(document.getElementById("fd_lebar_jendela").value) || 0;
    var fd_t_jendela = parseFloat(document.getElementById("fd_tinggi_jendela").value) || 0;
    var fd_j_jendela = parseFloat(document.getElementById("fd_jumlah_jendela").value) || 0;
    var p_fdinding_rusak = parseFloat(document.getElementById("panjang_fdinding_rusak").value) || 0;
    var l_fdindng_rusak = parseFloat(document.getElementById("lebar_fdinding_rusak").value) || 0;

    var fdinding_rsr = parseFloat(document.getElementById("fdinding_rsr").value) || 0;
    var fdinding_rr = parseFloat(document.getElementById("fdinding_rr").value) || 0;
    var fdinding_rs = parseFloat(document.getElementById("fdinding_rs").value) || 0;
    var fdinding_rb = parseFloat(document.getElementById("fdinding_rb").value) || 0;
    var fdinding_rsb = parseFloat(document.getElementById("fdinding_rsb").value) || 0;
    var fdinding_kts = parseFloat(document.getElementById("fdinding_kts").value) || 0;

    // Hitung luas
    var luas_fdinding = calculateAreaDinding(p_fdinding, t_fdinding);
    var fd_luas_pintu = calculateAreaPintuJendela(fd_l_pintu, fd_t_pintu, fd_j_pintu);
    var fd_luas_jendela = calculateAreaPintuJendela(fd_l_jendela, fd_t_jendela, fd_j_jendela);
    var luas_fdinding_rusak = calculateAreaDinding(p_fdinding_rusak, l_fdindng_rusak);

    // Hitung luas bidang tidak rusak
    var fdinding_tr = 100 - (fdinding_rsr + fdinding_rr + fdinding_rs + fdinding_rb + fdinding_rsb + fdinding_kts)

    // Update input luas
    document.getElementById("luas_fdinding").value = luas_fdinding.toFixed(2);
    document.getElementById("fd_luas_pintu").value = fd_luas_pintu.toFixed(2);
    document.getElementById("fd_luas_jendela").value = fd_luas_jendela.toFixed(2);
    document.getElementById("luas_fdinding_rusak").value = luas_fdinding_rusak.toFixed(2);
    document.getElementById("fdinding_tr").value = fdinding_tr;

    // Hitung persentase kerusakan (Luas Bidang Rusak / (Luas Dinding - Luas Pintu - Luas Jendela) * 100%)
    var total_luas_fdinding = luas_fdinding - (fd_luas_pintu + fd_luas_jendela);
    var kerusakan_fdinding = total_luas_fdinding ? (luas_fdinding_rusak / total_luas_fdinding) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_fdinding").value = kerusakan_fdinding.toFixed(2);
}

// Kalkulator Finishing Kupin
function calcFKupin() {
    function calculateAreaFKusen(tinggi, jpv, panjang, jph, tebal_balok, lebar_balok) {
        return tinggi && jpv && panjang && jph && tebal_balok && lebar_balok ? (tinggi * jpv) + (panjang * jph) * (tebal_balok * lebar_balok) : 0;
    }

    function calculateAreaFKPintu(tinggi, lebar, tebal, jumlah) {
        return tinggi && lebar && tebal ? (tinggi * lebar * tebal) * jumlah : 0;
    }

    function calculateAreaFKRusak(panjang, lebar) {
        return panjang && lebar ? panjang * lebar : 0;
    }

    // Ambil nilai input
    var t_kupin = parseFloat(document.getElementById("tinggi_kupin").value) || 0;
    var jpv_pintu = parseFloat(document.getElementById("jpv_kusen_pintu").value) || 0;
    var p_kupin = parseFloat(document.getElementById("panjang_kupin").value) || 0;
    var jph_pintu = parseFloat(document.getElementById("jph_kusen_pintu").value) || 0;
    var tb_kupin = parseFloat(document.getElementById("tebal_balok_kupin").value) || 0;
    var lb_kupin = parseFloat(document.getElementById("lebar_balok_kupin").value) || 0;

    var t_kujen = parseFloat(document.getElementById("tinggi_kujen").value) || 0;
    var jpv_jendela = parseFloat(document.getElementById("jpv_kusen_jendela").value) || 0;
    var p_kujen = parseFloat(document.getElementById("panjang_kujen").value) || 0;
    var jph_jendela = parseFloat(document.getElementById("jph_kusen_jendela").value) || 0;
    var tb_kujen = parseFloat(document.getElementById("tebal_balok_kujen").value) || 0;
    var lb_kujen = parseFloat(document.getElementById("lebar_balok_kujen").value) || 0;

    var fk_tinggi_pintu = parseFloat(document.getElementById("fk_tinggi_pintu").value) || 0;
    var fk_lebar_pintu = parseFloat(document.getElementById("fk_lebar_pintu").value) || 0;
    var fk_jumlah_pintu = parseFloat(document.getElementById("fk_jumlah_pintu").value) || 0;
    var p_Finishing_rusak = parseFloat(document.getElementById("panjang_fkupin_rusak").value) || 0;
    var l_Finishing_rusak = parseFloat(document.getElementById("lebar_fkupin_rusak").value) || 0;

    var fkupin_rsr = parseFloat(document.getElementById("fkupin_rsr").value) || 0;
    var fkupin_rr = parseFloat(document.getElementById("fkupin_rr").value) || 0;
    var fkupin_rs = parseFloat(document.getElementById("fkupin_rs").value) || 0;
    var fkupin_rb = parseFloat(document.getElementById("fkupin_rb").value) || 0;
    var fkupin_rsb = parseFloat(document.getElementById("fkupin_rsb").value) || 0;
    var fkupin_kts = parseFloat(document.getElementById("fkupin_kts").value) || 0;

    // Hitung Volume
    var volume_kupin = calculateAreaFKusen(t_kupin, jpv_pintu, p_kupin, jph_pintu, tb_kupin, lb_kupin);
    var volume_kujen = calculateAreaFKusen(t_kujen, jpv_jendela, p_kujen, jph_jendela, tb_kujen, lb_kujen);
    var volume_pintu = calculateAreaFKPintu(fk_tinggi_pintu, fk_lebar_pintu, fk_lebar_pintu, fk_jumlah_pintu)
    var luas_fkupin_rusak = calculateAreaFKRusak(p_Finishing_rusak, l_Finishing_rusak)

    // Hitung luas bidang tidak rusak
    var fkupin_tr = 100 - (fkupin_rsr + fkupin_rr + fkupin_rs + fkupin_rb + fkupin_rsb + fkupin_kts)

    // Update input Volume
    document.getElementById("volume_kupin").value = volume_kupin;
    document.getElementById("volume_kujen").value = volume_kujen;
    document.getElementById("fk_volume_pintu").value = volume_pintu;
    document.getElementById("luas_fkupin_rusak").value = luas_fkupin_rusak;
    document.getElementById("fkupin_tr").value = fkupin_tr;

    // Hitung persentase kerusakan (Volume Bidang Rusak / (Volume kupin + Volume kujen + Volume pintu) * 100%)
    var total_Volume_Finishing = volume_kupin + volume_kujen + volume_pintu;
    var kerusakan_fkupin = total_Volume_Finishing ? (luas_fkupin_rusak / total_Volume_Finishing) * 100 : 0;

    // Tampilkan hasil
    document.getElementById("kerusakan_fkupin").value = kerusakan_fkupin.toFixed(2);
}