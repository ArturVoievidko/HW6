import json
from pathlib import Path
from normalize import normalize
import sys
import shutil
import os



CATEGORIES = None
result = {"archive": [], "music": [], "documents": [], "imagines": [], "uknown": [], "formats": set(), "unknownfomats": set()}

def read_folders(path: Path) -> list[Path]:
    return list(path.glob('**/*'))[::-1]

def create_target_folders(path: Path, categories: dict) -> list[Path]:
    target_folders_path = []
    for i in categories:
        if not path.joinpath(i).exists():
            path.joinpath(i).mkdir(parents=True)
            target_folders_path.append(path.joinpath(i))
    return target_folders_path

def create_categories(path: str) -> dict:
    with open(path) as f:
        result = json.load(f)
    return result



def rename_files(name: str) -> str:
    new_name = normalize(name)         
    return new_name    

def archive(path: Path) -> str:
    ...

def delete_folders(path: Path) -> str:
    #Deleta empty folder
    path.rmdir()


def sort_files(lst: list[Path], path: Path) -> str:
    CATEGORIES = create_categories("cat.json")
    #keys = [k for k in CATEGORIES]
    
    for item in lst:
        if item.is_dir():
            if not os.listdir(item):
                os.rmdir(item)
        elif item.suffix in CATEGORIES["archive"]:
            new_dir = path.joinpath("archive", item.name)
            os.mkdir(new_dir)
            shutil.unpack_archive(item, new_dir)
            result["archive"].append(new_dir)
            result["formats"].add(item.suffix)
            os.remove(item)

        elif item.suffix in CATEGORIES["music"]:
            new_name = path.joinpath("music", rename_files(item.name))
            os.rename(item, new_name)
            result["music"].append(new_name)
            result["formats"].add(item.suffix)
        elif item.suffix in CATEGORIES["documents"]:
            new_name = path.joinpath("documents", rename_files(item.name))
            os.rename(item, new_name)
            result["documents"].append(new_name)
            result["formats"].add(item.suffix)
        elif item.suffix in CATEGORIES["imagines"]:
            new_name = path.joinpath("imagines", rename_files(item.name))
            os.rename(item, new_name)
            result["imagines"].append(new_name)
            result["formats"].add(item.suffix)
        else:
            new_name = path.joinpath("uknown", rename_files(item.name))
            os.rename(item, new_name)
            result["uknown"].append(new_name)
            result["unknownfomats"].add(item.suffix)
    
        # for k in keys:
        #     suffix = item.suffix
        #     if suffix in CATEGORIES[k]:
        #         print(f"file is {k}")
        #         #shutil.move(item, path.joinpath(k))
        #         new_name = path.joinpath(k, rename_files(item.name))
        #         print(new_name)
        #         os.rename(item, new_name)


def main() -> str:
    path = None
    try: 
        path = Path(sys.argv[1])
    except IndexError:
        print("No param")
    CATEGORIES = create_categories("cat.json")
    files = read_folders(path)
    create_target_folders(path, CATEGORIES)
    sort_files(files, path)
    for k, v in result.items():
        print(k)
        for c in v:
            print(c)




if __name__ == "__main__":
    main()
