import sys
from typing import Any
from pydantic import Field, BaseModel, model_validator, ValidationError


class KeyValidation(BaseModel):
    """
    class with pydantic 'BaseModel' to check key and value
    """
    WIDTH: int = Field(ge=1)
    HEIGHT: int = Field(ge=1)
    ENTRY: str
    EXIT: str
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = Field(default=None)
    WINDOW: int | None = Field(ge=1, le=3, default=None)

    @model_validator(mode="after")
    def model_validator(self) -> Any:
        """
        validation of value
        """
        en_x, en_y = map(int, self.ENTRY.split(","))
        ex_x, ex_y = map(int, self.EXIT.split(","))
        if en_x < 0 or en_y < 0:
            raise ValueError("entry can't be below 0")
        if en_x >= self.WIDTH or en_y >= self.HEIGHT:
            raise ValueError("entry can't be above width or height")
        if ex_x < 0 or ex_y < 0:
            raise ValueError("exit can't be below 0")
        if ex_x >= self.WIDTH or ex_y >= self.HEIGHT:
            raise ValueError("exit can't be above width or height")
        if not self.OUTPUT_FILE.endswith('.txt'):
            raise ValueError("output file must be ending by '.txt'")
        if ex_y == en_y and en_x == ex_x:
            raise ValueError("entry can't be same than exit")
        return self

    def return_dict(self) -> dict[str, Any]:
        """
        create dict of data config after validation
        """
        config_dict: dict[str, Any] = {}
        config_dict["WIDTH"] = self.WIDTH
        config_dict["HEIGHT"] = self.HEIGHT
        config_dict["ENTRY"] = map(int, self.ENTRY.split(","))
        config_dict["EXIT"] = map(int, self.EXIT.split(","))
        config_dict["PERFECT"] = self.PERFECT
        config_dict["WINDOW"] = self.WINDOW
        config_dict["SEED"] = self.SEED
        config_dict["OUTPUT_FILE"] = self.OUTPUT_FILE
        return config_dict


def read_file() -> tuple[list[str], str]:
    """
    function take arg 'file_name' and read file
    """
    args = sys.argv[1:]
    file_name = sys.argv[1]
    if len(args) != 1:
        raise ValueError("error args")
    try:
        with open(args[0], "r") as f:
            result = f.read()
            if result:
                lst = result.splitlines()
                return lst, file_name
            raise ValueError("file empty")
    except IOError as e:
        raise ValueError(f"ERROR: {e}")


def pars_args(args: list[str]) -> dict[str, Any]:
    """
    function to pars arg like dict[key, value] and check if keys exists
    """
    key: list[str] = [
        "WIDTH", "HEIGHT", "ENTRY",
        "EXIT", "PERFECT", "WINDOW", "SEED", "OUTPUT_FILE"]
    inventory: dict[str, Any] = {}
    if args:
        try:
            for item in args:
                if not item or item.startswith("#"):
                    continue
                name, value = item.split("=")
                if name not in key:
                    raise ValueError(f"key: '{name}' can't be in config file")
                inventory[name] = value.strip()
        except Exception as e:
            raise ValueError(f"error : {e}")
    return inventory


def pars_dict() -> dict[str, Any]:
    """
    manage all fuction of parsing and return the right dict of data
    """
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
