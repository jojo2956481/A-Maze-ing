import sys
from typing import Any
from pydantic import Field, BaseModel, model_validator, ValidationError


class KeyValidation(BaseModel):
    WIDTH: int = Field(ge=9)
    HEIGHT: int = Field(ge=7)
    ENTRY: str
    EXIT: str
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = Field(default=None)
    WINDOW: int | None = Field(ge=1, le=3, default=None)

    @model_validator(mode="after")
    def model_validator(self) -> Any:
        en_x, en_y = map(int, self.ENTRY.split(","))
        ex_x, ex_y = map(int, self.EXIT.split(","))
        if en_x < 0 or en_y < 0:
            raise ValueError("entry can't be below 0")
        if ex_x < 0 or ex_y < 0:
            raise ValueError("exit can't be below 0")
        if ex_x > self.WIDTH or ex_y > self.HEIGHT:
            raise ValueError("exit can´t be above width or height")
        if self.OUTPUT_FILE.endswith('.txt\n'):
            raise ValueError("output file must be ending by '.txt'")
        else:
            return self

    def return_dict(self) -> dict[str, Any]:
        config_dict: dict[str, Any] = {}
        config_dict["WIDTH"] = self.WIDTH
        config_dict["HEIGHT"] = self.HEIGHT
        config_dict["ENTRY"] = map(int, self.ENTRY.split(","))
        config_dict["EXIT"] = map(int, self.EXIT.split(","))
        config_dict["PERFECT"] = self.PERFECT
        config_dict["WINDOW"] = self.WINDOW
        config_dict["SEED"] = self.SEED
        return config_dict


def read_file() -> tuple[list[str], str]:
    args = sys.argv[1:]
    file_name = sys.argv[1]
    if len(args) != 1:
        raise ValueError("error args")
    try:
        with open(args[0], "r") as f:
            contenue = f.read()
            if contenue:
                lst = contenue.splitlines()
                return lst, file_name
            raise ValueError("file empty")
    except IOError as e:
        raise ValueError(f"ERROR: {e}")


def pars_args(args: list[str]) -> dict[str, Any]:
    inventory: dict[str, Any] = {}
    if args:
        try:
            for item in args:
                if not item or item.startswith("#"):
                    continue
                name, value = item.split("=")
                inventory[name] = value.strip()
        except Exception as e:
            raise ValueError(f"error : {e}")
    return inventory


def pars_dict() -> dict[str, Any] | None:
    try:
        data, file_name = read_file()
        data_dict = pars_args(data)
        config = KeyValidation(**data_dict)
        if config.OUTPUT_FILE == file_name:
            print(
                "error output file must"
                " be different than config file")
            sys.exit(0)
    except ValidationError as e:
        print(e.errors()[0]['msg'])
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)
    else:
        return config.return_dict()
