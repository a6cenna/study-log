import json
from datetime import datetime
from collections import defaultdict

catatan = []
target_harian = {}  # {mapel: durasi_menit}
file_data = "catatan.json"

# ===== FUNGSI UTAMA =====

def tambah_catatan():
    """Menambahkan catatan belajar baru"""
    print("\n--- Tambah Catatan Belajar ---")
    
    mapel = input("Masukkan nama mapel: ").strip()
    if not mapel:
        print("❌ Mapel tidak boleh kosong!")
        return
    
    topik = input("Masukkan topik: ").strip()
    if not topik:
        print("❌ Topik tidak boleh kosong!")
        return
    
    try:
        durasi = int(input("Masukkan durasi belajar (menit): ").strip())
        if durasi <= 0:
            print("❌ Durasi harus lebih dari 0!")
            return
    except ValueError:
        print("❌ Durasi harus berupa angka!")
        return
    
    catatan_baru = {
        "mapel": mapel,
        "topik": topik,
        "durasi": durasi,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    catatan.append(catatan_baru)
    print(f"✅ Catatan '{mapel}' berhasil ditambahkan!")
    simpan_ke_file()


def lihat_catatan():
    """Menampilkan semua catatan dengan format rapi"""
    if not catatan:
        print("\n📭 Belum ada catatan belajar. Mulai belajar sekarang!")
        return
    
    print("\n=== Daftar Catatan Belajar ===")
    print("-" * 70)
    print(f"{'No.':<4} {'Mapel':<15} {'Topik':<20} {'Durasi':<10} {'Tanggal':<15}")
    print("-" * 70)
    
    for i, c in enumerate(catatan, 1):
        print(f"{i:<4} {c['mapel']:<15} {c['topik']:<20} {c['durasi']} menit  {c['tanggal']}")
    
    print("-" * 70)


def total_waktu():
    """Menghitung total durasi belajar"""
    if not catatan:
        print("\n📭 Belum ada catatan belajar.")
        return
    
    total = sum(c["durasi"] for c in catatan)
    jam = total // 60
    menit = total % 60
    
    print(f"\n⏱️  Total waktu belajar: {total} menit ({jam} jam {menit} menit)")
    
    # Statistik per mapel
    print("\n📊 Durasi per mapel:")
    mapel_durasi = defaultdict(int)
    for c in catatan:
        mapel_durasi[c["mapel"]] += c["durasi"]
    
    for mapel, durasi in sorted(mapel_durasi.items(), key=lambda x: x[1], reverse=True):
        jam_mapel = durasi // 60
        menit_mapel = durasi % 60
        print(f"  • {mapel}: {durasi} menit ({jam_mapel}h {menit_mapel}m)")


def set_target_harian():
    """Mengatur target belajar harian per mapel"""
    print("\n--- Set Target Harian ---")
    mapel = input("Masukkan nama mapel: ").strip()
    
    try:
        target = int(input("Masukkan target durasi (menit): ").strip())
        if target <= 0:
            print("❌ Target harus lebih dari 0!")
            return
        
        target_harian[mapel] = target
        print(f"✅ Target untuk {mapel} diatur: {target} menit")
        simpan_ke_file()
    except ValueError:
        print("❌ Target harus berupa angka!")


def lihat_target():
    """Menampilkan target harian"""
    if not target_harian:
        print("\n📭 Belum ada target harian yang diatur.")
        return
    
    print("\n🎯 Target Harian Belajar:")
    print("-" * 40)
    for mapel, target in sorted(target_harian.items()):
        print(f"  {mapel}: {target} menit/hari")
    print("-" * 40)


def ringkasan_mingguan():
    """Menampilkan ringkasan belajar mingguan per mapel"""
    if not catatan:
        print("\n📭 Belum ada catatan belajar.")
        return
    
    print("\n📅 Ringkasan Mingguan Belajar:")
    print("-" * 50)
    
    mapel_data = defaultdict(lambda: {"total": 0, "topik": []})
    
    for c in catatan:
        mapel_data[c["mapel"]]["total"] += c["durasi"]
        if c["topik"] not in mapel_data[c["mapel"]]["topik"]:
            mapel_data[c["mapel"]]["topik"].append(c["topik"])
    
    for mapel in sorted(mapel_data.keys()):
        data = mapel_data[mapel]
        jam = data["total"] // 60
        menit = data["total"] % 60
        print(f"\n📚 {mapel}")
        print(f"   Total: {data['total']} menit ({jam}h {menit}m)")
        print(f"   Topik yang dipelajari:")
        for topik in data["topik"]:
            print(f"     • {topik}")
    
    print("\n" + "-" * 50)


# ===== FUNGSI PENYIMPANAN =====

def simpan_ke_file():
    """Menyimpan data ke file JSON"""
    data = {
        "catatan": catatan,
        "target_harian": target_harian,
        "terakhir_diupdate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(file_data, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 Data berhasil disimpan!")
    except Exception as e:
        print(f"❌ Error menyimpan file: {e}")


def muat_dari_file():
    """Memuat data dari file JSON"""
    global catatan, target_harian
    
    try:
        with open(file_data, "r", encoding="utf-8") as f:
            data = json.load(f)
            catatan = data.get("catatan", [])
            target_harian = data.get("target_harian", {})
        print("✅ Data berhasil dimuat!")
    except FileNotFoundError:
        print("📝 File data tidak ditemukan, membuat file baru...")
    except Exception as e:
        print(f"⚠️  Error membaca file: {e}")


# ===== MENU =====

def menu():
    print("\n" + "="*40)
    print("      🎓 STUDY LOG APP 🎓")
    print("="*40)
    print("1. Tambah catatan belajar")
    print("2. Lihat semua catatan")
    print("3. Total waktu belajar")
    print("4. Set target harian")
    print("5. Lihat target harian")
    print("6. Ringkasan mingguan")
    print("7. Keluar")
    print("="*40)


# ===== MAIN PROGRAM =====

if __name__ == "__main__":
    muat_dari_file()
    
    while True:
        menu()
        pilihan = input("Pilih menu (1-7): ").strip()

        if pilihan == "1":
            tambah_catatan()
        elif pilihan == "2":
            lihat_catatan()
        elif pilihan == "3":
            total_waktu()
        elif pilihan == "4":
            set_target_harian()
        elif pilihan == "5":
            lihat_target()
        elif pilihan == "6":
            ringkasan_mingguan()
        elif pilihan == "7":
            print("\n✨ Terima kasih, terus semangat belajar! ✨")
            simpan_ke_file()
            break
        else:
            print("❌ Pilihan tidak valid! Silakan coba lagi.")