from datetime import datetime

# =====================================================================
# 1. LIST
# =====================================================================

daftar_nip = ["1001", "1002", "1003", "1004", "1005"]
daftar_nama = [
    "Tri Margaretha Tarigan",
    "Muchammad Raditya El Athallah",
    "Megantara Abdillah Persada",
    "Jasiro Haq Darmawan",
    "Gusti Ayu Kirana Putri Airlangga",
]

fp_terdaftar = []
nip_fp_terdaftar = []
log_absensi = []
data_katering = []


# =====================================================================
# 2. SUBPROGRAM BANTUAN & INPUT JAM SIMULASI
# =====================================================================

def minta_jam_simulasi():
    while True:
        jam_teks = input("Masukkan jam simulasi (HH:MM, contoh 08:30): ").strip()
        try:
            return datetime.strptime(jam_teks, "%H:%M").time()
        except ValueError:
            print("-> Format jam salah! Gunakan format HH:MM (contoh: 08:30 atau 17:15).")


def cari_nama_pegawai(nip_cari):
    for i in range(len(daftar_nip)):
        if daftar_nip[i] == nip_cari:
            return daftar_nama[i]
    return None


def cari_nip_dari_fp(kode_fp):
    for i in range(len(fp_terdaftar)):
        if fp_terdaftar[i] == kode_fp:
            return nip_fp_terdaftar[i]
    return None


def cek_sudah_absen_pagi(nip_cari):
    for log in log_absensi:
        if log[0] == nip_cari and log[2] == "pagi":
            return True
    return False


# =====================================================================
# 3. SUBPROGRAM PENDAFTARAN SIDIK JARI
# =====================================================================

def daftar_sidik_jari():
    print("\n--- PENDATAAN SIDIK JARI ---")
    while True:
        lanjut = input("Ingin mendaftarkan sidik jari? (y/t): ").strip().lower()
        if lanjut != "y":
            break

        kode_input = input("Masukkan Kode Sidik Jari (contoh: FP-A): ").strip()
        nip_input = input("Masukkan NIP Karyawan (1001-1005): ").strip()

        nama_pegawai = cari_nama_pegawai(nip_input)
        if nama_pegawai is None:
            print("-> PENDAFTARAN DITOLAK: NIP tidak terdaftar di perusahaan!\n")
        else:
            fp_terdaftar.append(kode_input)
            nip_fp_terdaftar.append(nip_input)
            print(f"-> BERHASIL: Sidik jari {kode_input} terdaftar atas nama {nama_pegawai}\n")

    print(f"[INFO] Total sidik jari terdaftar saat ini: {len(fp_terdaftar)}")


# =====================================================================
# 4. SUBPROGRAM ABSENSI & KONFIRMASI KATERING
# =====================================================================

def proses_konfirmasi_katering(nip_pegawai, nama_pegawai, waktu_scan, jam_9_pagi):
    if waktu_scan <= jam_9_pagi:
        mau_makan = input("Pesan jatah makan siang hari ini? (y/t): ").strip().lower()
        if mau_makan == "y":
            data_katering.append([nip_pegawai, nama_pegawai, "ya", "belum", "-"])
            print("-> Katering: Jatah makan siang TERKONFIRMASI.")
        else:
            data_katering.append([nip_pegawai, nama_pegawai, "tidak", "tidak", "-"])
            print("-> Katering: Tidak pesan makan siang (mengurangi food waste).")
    else:
        data_katering.append([nip_pegawai, nama_pegawai, "tidak", "tidak", "-"])
        print("-> Katering: Lewat jam 09:00, tidak masuk kuota makan siang hari ini.")


def proses_absen_pagi(nip_pegawai, nama_pegawai, waktu_scan):
    jam_9_pagi = datetime.strptime("09:00", "%H:%M").time()
    jam_10_pagi = datetime.strptime("10:00", "%H:%M").time()

    if waktu_scan <= jam_9_pagi:
        status_absen = "Hadir tepat waktu"
    elif waktu_scan <= jam_10_pagi:
        status_absen = "Hadir terlambat"
    else:
        print("-> Keterangan: Tidak tercatat / Telat Absen\n")
        return

    jam_str = waktu_scan.strftime("%H:%M")
    log_absensi.append([nip_pegawai, nama_pegawai, "pagi", jam_str, status_absen])
    print(f"-> BERHASIL: {status_absen} untuk {nama_pegawai} (pagi)")

    proses_konfirmasi_katering(nip_pegawai, nama_pegawai, waktu_scan, jam_9_pagi)
    print()


def proses_absen_pulang(nip_pegawai, nama_pegawai, waktu_scan):
    jam_10_pagi = datetime.strptime("10:00", "%H:%M").time()
    jam_17_sore = datetime.strptime("17:00", "%H:%M").time()

    if waktu_scan <= jam_10_pagi:
        print("-> Keterangan: Sudah absen pagi\n")
    elif waktu_scan < jam_17_sore:
        print("-> Keterangan: Belum waktu pulang\n")
    else:
        jam_str = waktu_scan.strftime("%H:%M")
        log_absensi.append([nip_pegawai, nama_pegawai, "pulang", jam_str, "Kepulangan tercatat"])
        print(f"-> BERHASIL: Kepulangan tercatat untuk {nama_pegawai} (pulang)\n")


def scan_absensi():
    print("\n--- SCAN ABSENSI HARIAN (SIMULASI) ---")
    while True:
        lanjut = input("Lakukan scan absensi sekarang? (y/t): ").strip().lower()
        if lanjut != "y":
            break

        kode_scan = input("Masukkan Kode Sidik Jari yang di-scan: ").strip()
        nip_karyawan = cari_nip_dari_fp(kode_scan)

        if nip_karyawan is None:
            print("-> GAGAL: Sidik jari tidak dikenal / belum didata!\n")
            continue

        nama_karyawan = cari_nama_pegawai(nip_karyawan)
        waktu_scan = minta_jam_simulasi()
        print(f"-> Waktu simulasi: {waktu_scan.strftime('%H:%M')} WIB")

        if cek_sudah_absen_pagi(nip_karyawan):
            proses_absen_pulang(nip_karyawan, nama_karyawan, waktu_scan)
        else:
            proses_absen_pagi(nip_karyawan, nama_karyawan, waktu_scan)


# =====================================================================
# 5. SUBPROGRAM AMBIL MAKAN SIANG (LUNCH TAGGING)
# =====================================================================

def ambil_makan_siang():
    print("\n--- VALIDASI AMBIL MAKAN SIANG (SIMULASI) ---")
    while True:
        lanjut = input("Ada karyawan ambil makan siang? (y/t): ").strip().lower()
        if lanjut != "y":
            break

        kode_scan = input("Masukkan Kode Sidik Jari: ").strip()
        nip_karyawan = cari_nip_dari_fp(kode_scan)

        if nip_karyawan is None:
            print("-> GAGAL: Sidik jari tidak dikenal!\n")
            continue

        waktu_scan = minta_jam_simulasi()
        jam_mulai = datetime.strptime("12:00", "%H:%M").time()
        jam_selesai = datetime.strptime("14:00", "%H:%M").time()

        if waktu_scan < jam_mulai or waktu_scan > jam_selesai:
            print("-> INFO: Di luar jam makan siang (12:00 - 14:00 WIB).\n")
            continue

        ditemukan = False
        for item in data_katering:
            if item[0] == nip_karyawan:
                ditemukan = True
                if item[2] != "ya":
                    print(f"-> DITOLAK: {item[1]} tidak punya kuota makan siang hari ini.\n")
                elif item[3] == "sudah":
                    print(f"-> DITOLAK (DOUBLE CLAIM): {item[1]} sudah ambil jam {item[4]} WIB!\n")
                else:
                    item[3] = "sudah"
                    item[4] = waktu_scan.strftime("%H:%M")
                    print(f"-> BERHASIL: Silakan ambil makan siang, {item[1]} ({item[4]} WIB).\n")
                break

        if not ditemukan:
            print("-> DITOLAK: Belum absen pagi / belum konfirmasi makan siang.\n")


# =====================================================================
# 6. SUBPROGRAM REKAP AKHIR
# =====================================================================

def tampilkan_rekap():
    print("\n" + "=" * 45)
    print("=== REKAP LAPORAN ABSENSI HARI INI ===")
    print("=" * 45)

    if len(log_absensi) == 0:
        print("Belum ada data absensi yang tercatat.")
    else:
        for nomor, data in enumerate(log_absensi, start=1):
            print(f"{nomor}. {data[1]} | Jenis: {data[2]} | Jam: {data[3]} WIB | Status: {data[4]}")

    print("\n" + "=" * 45)
    print("=== REKAP KUOTA KATERING HARI INI ===")
    print("=" * 45)

    total_pesanan = 0
    total_diambil = 0

    for item in data_katering:
        if item[2] == "ya":
            total_pesanan += 1
        if item[3] == "sudah":
            total_diambil += 1

    print(f"Total porsi katering dipesan : {total_pesanan}")
    print(f"Total porsi sudah diambil    : {total_diambil}")
    print(f"Sisa belum diambil           : {total_pesanan - total_diambil}")


# =====================================================================
# 7. PROGRAM UTAMA DENGAN MENU
# =====================================================================

print("=== PROGRAM SISTEM ABSENSI & KATERING OTOMATIS (VERSI SIMULASI) ===")
daftar_sidik_jari()

while True:
    print("\n=== MENU UTAMA ===")
    print("1. Scan Absensi (Pagi / Pulang)")
    print("2. Validasi Ambil Makan Siang")
    print("3. Lihat Rekap Sementara")
    print("4. Selesai & Tampilkan Rekap Akhir")
    pilih = input("Pilih menu (1/2/3/4): ").strip()

    if pilih == "1":
        scan_absensi()
    elif pilih == "2":
        ambil_makan_siang()
    elif pilih == "3":
        tampilkan_rekap()
    elif pilih == "4":
        tampilkan_rekap()
        break
    else:
        print("-> Pilihan tidak valid, coba lagi.")

print("\nProgram Selesai.")