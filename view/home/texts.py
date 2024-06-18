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
            return "🥰私たちって似てる？"
        elif self.is_en:
            return "🥰Do We Look Alike?"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def authers(self) -> str:
        return "Created by [Takanari Shimbo 🦥](https://github.com/TakanariShimbo), [Shunichi Ikezu 🍓](https://github.com/ikeshun15)"

    @property
    def downloading_model(self) -> str:
        if self.is_jp:
            return "モデルダウンロード中..."
        elif self.is_en:
            return "Downloading Model..."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

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
    def please_upload_photo_of_person1(self) -> str:
        if self.is_jp:
            return "一人目の写真をアップロードしてね"
        elif self.is_en:
            return "Please upload 'Photo of Person 1'"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def please_upload_photo_of_person2(self) -> str:
        if self.is_jp:
            return "二人目の写真をアップロードしてね"
        elif self.is_en:
            return "Please upload 'Photo of Person 2'"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def analyze(self) -> str:
        if self.is_jp:
            return "解析する✨"
        elif self.is_en:
            return "Analyze✨"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def analyzing(self) -> str:
        if self.is_jp:
            return "解析中..."
        elif self.is_en:
            return "Analyzing..."
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def only_one_person(self) -> str:
        if self.is_jp:
            return "誰か一人が映っている写真にしてね"
        elif self.is_en:
            return "Please make sure the photo contains only one person"
        raise Exception("lang at Texts should be 'ja' or 'en'!")

    @property
    def change_lang(self) -> str:
        if self.is_jp:
            return "🗾言語切替"
        elif self.is_en:
            return "🗽Language"
        raise Exception("lang at Texts should be 'ja' or 'en'!")
