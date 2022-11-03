from bot.config import get_settings

settings = get_settings()


class Mode:
    spam: str = settings.SPAM_MODE
    registry: str = settings.REGISTRY_MODE
    workflow: str = settings.WORKFLOW_MODE
    summary: str = settings.SUMMARY_MODE

    @classmethod
    def to_dict(cls):
        return {
            cls.spam: "spam",
            cls.registry: "registry",
            cls.workflow: "workflow",
            cls.summary: "summary",
        }


def change_mode(new_mode) -> str | None:
    if new_mode not in Mode().to_dict().keys():
        return None
    else:
        settings.CURRENT_MODE = new_mode
        return f"Changed to {Mode().to_dict()[new_mode]}"
