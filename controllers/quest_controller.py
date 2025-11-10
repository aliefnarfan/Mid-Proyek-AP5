# Controller for quest
import random
from models.quest_model import QuestData

class QuestController:
    def __init__(self, character):
        self.character = character
        self.active_quest = None

    def bikin_quest(self):
        # Jika sudah menyelesaikan 3 quest biasa, munculkan quest boss
        if self.karakter.quest_selesai >= 3:
            self.buat_quest_boss()
            self.karakter.quest_selesai = 0  # reset counter setelah boss
            return

        tipe_quest = random.choice(["berburu", "pengumpulan"])
        kesulitan = random.choice(["mudah", "sedang", "sulit"])
        pengali = {"mudah": 1, "sedang": 1.5, "sulit": 2}[kesulitan]

        if tipe_quest == "berburu":
            musuh = random.choice(["goblin", "serigala", "bandit", "orc", "naga kecil"])
            gold_reward = int(random.randint(5, 15) * pengali)
            exp_reward = int(random.randint(10, 25) * pengali)
            quest = QuestData("berburu", f"Lawan {musuh}", gold_reward, exp_reward, kesulitan)

        else:
            material = random.choice(["kayu", "batu sihir", "herbal", "kulit binatang", "bijih besi"])
            gold_reward = int(random.randint(3, 10) * pengali)
            exp_reward = int(random.randint(8, 20) * pengali)
            quest = QuestData("pengumpulan", f"Kumpulkan {material}", gold_reward, exp_reward, kesulitan)

        self.active_quest = quest
        print("\nQuest Baru Diterima!")
        quest.tampilkan_info_quest()

    def selesaikan_quest(self):
        if not self.active_quest:
            print("❌ Tidak ada quest aktif!\n")
            return

        print(f"Menjalankan quest: {self.active_quest.nama}...")
        hasil = random.choices(["berhasil", "gagal"], weights=[0.8, 0.2])[0]

        if hasil == "berhasil":
            self.character.gold += self.active_quest.reward_gold
            self.character.exp += self.active_quest.reward_exp
            print(f"✅ Quest selesai! Kamu mendapat {self.active_quest.reward_gold} gold dan {self.active_quest.reward_exp} exp.")
            self.level_up()
        else:
            print("❌ Quest gagal! Tidak mendapat hadiah.")

        self.active_quest = None
        print(f"💰 Gold: {self.character.gold} | ⭐ EXP: {self.character.exp}\n")

    def buat_quest_boss(self):
        bos = random.choice(["Naga Api", "Raja Orc", "Iblis Kegelapan", "Hydra"])
        print("\n🔥 QUEST BOSS TERBUKA! 🔥")
        hadiah_uang = random.randint(50, 100)
        hadiah_exp = random.randint(150, 250)
        quest_boss = QuestData("boss", f"Kalahkan {bos}", hadiah_uang, hadiah_exp, "epik")
        self.quest_aktif = quest_boss
        self.karakter.bisa_lawan_boss = True
        quest_boss.tampilkan_info_quest()

    def selesaikan_quest(self):
        if not self.quest_aktif:
            print("❌ Tidak ada quest aktif!\n")
            return

        print(f"Menjalankan quest: {self.quest_aktif.nama}...")
        hasil = random.choices(["berhasil", "gagal"], weights=[0.8, 0.2])[0]

        if hasil == "berhasil":
            self.karakter.uang += self.quest_aktif.hadiah_uang
            self.karakter.pengalaman += self.quest_aktif.hadiah_exp
            print(f"✅ Quest berhasil! Kamu mendapat {self.quest_aktif.hadiah_uang} gold dan {self.quest_aktif.hadiah_exp} exp.")

            if self.quest_aktif.tipe == "boss":
                self.level_up_setelah_boss()
            else:
                self.karakter.quest_selesai += 1
                print(f"📜 Quest selesai: {self.karakter.quest_selesai}/3 sebelum boss muncul.")

        else:
            print("❌ Quest gagal! Tidak mendapat hadiah.")

        self.quest_aktif = None
        print(f"💰 Gold: {self.karakter.uang} | ⭐ EXP: {self.karakter.pengalaman}\n")

    def level_up_setelah_boss(self):
        print("👑 Kamu mengalahkan BOS! Pengalaman dan hadiah besar diterima.")
        self.karakter.level += 1
        self.karakter.gelar = random.choice(["Pahlawan", "Sang Penakluk", "Kesatria Agung", "Pembasmi Kegelapan"])
        self.karakter.bisa_lawan_boss = False
        print(f"🎉 LEVEL UP! Sekarang Level {self.karakter.level} - Gelar: {self.karakter.gelar}\n")
