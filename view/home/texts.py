from typing import Literal


class Texts:
    def __init__(self, lang: Literal["jp", "en"]) -> None:
        self._lang = lang

    @property
    def is_jp(self) -> bool:
        return self._lang == "jp"

    @property
    def is_en(self) -> bool:
        return self._lang == "en"

    @property
    def title(self) -> str:
        if self.is_jp:
            return "🥰 私たちって似てる？"
        elif self.is_en:
            return "🥰 Do We Look Alike?"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def authers(self) -> str:
        return "Created by [🦥 Takanari Shimbo](https://github.com/TakanariShimbo), [🍓 Shunichi Ikezu](https://github.com/ikeshun15)"

    @property
    def photo_of_person1(self) -> str:
        if self.is_jp:
            return "一人目の写真"
        elif self.is_en:
            return "Photo of Person 1"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def photo_of_person2(self) -> str:
        if self.is_jp:
            return "二人目の写真"
        elif self.is_en:
            return "Photo of Person 2"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def warning_no_person(self) -> str:
        if self.is_jp:
            return "🙅 一人以上映っている写真にしてね"
        elif self.is_en:
            return "🙅 Please make sure the photo includes more than one person."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def change_lang(self) -> str:
        if self.is_jp:
            return "🗾 言語切替"
        elif self.is_en:
            return "🗽 Language"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def back(self) -> str:
        if self.is_jp:
            return "⏪ 戻る"
        elif self.is_en:
            return "⏪ Back"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def others(self) -> str:
        if self.is_jp:
            return "🚶‍➡️ 他の人"
        elif self.is_en:
            return "🚶‍➡️ Others"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def next(self) -> str:
        if self.is_jp:
            return "⏭️ 進む"
        elif self.is_en:
            return "⏭️ Next"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def skip(self) -> str:
        if self.is_jp:
            return "⏭️ スキップ"
        elif self.is_en:
            return "⏭️ Skip"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def warning_same_person(self) -> str:
        if self.is_jp:
            return "🙅 一人目と違う人を選択してね"
        elif self.is_en:
            return "🙅 Please select someone different from the first."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def retry(self) -> str:
        if self.is_jp:
            return "🙋 もう一回"
        elif self.is_en:
            return "🙋 Retry"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def uploade_image1(self) -> str:
        if self.is_jp:
            return "一人目の写真をアップロードしてね"
        elif self.is_en:
            return "Please upload a photo of the first person."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def select_image1(self) -> str:
        if self.is_jp:
            return "一人目の顔写真を選んでね"
        elif self.is_en:
            return "Please select a photo of the first person's face."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def uploade_image2(self) -> str:
        if self.is_jp:
            return "二人目の写真をアップロードしてね"
        elif self.is_en:
            return "Please upload a photo of the second person."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def select_image2(self) -> str:
        if self.is_jp:
            return "二人目の顔写真を選んでね"
        elif self.is_en:
            return "Please select a photo of the second person's face."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def result(self) -> str:
        if self.is_jp:
            return "類似度は..."
        elif self.is_en:
            return "Similarity is ..."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def loading(self) -> str:
        if self.is_jp:
            return "読み込み中..."
        elif self.is_en:
            return "loading..."
        raise Exception("lang at Texts should be 'ja' or 'en'!")
