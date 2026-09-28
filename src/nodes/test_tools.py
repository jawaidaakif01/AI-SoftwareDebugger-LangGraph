from src.tools import list_files, read_file, search_in_repo

print(list_files.invoke({"folder": "sample_broken_repo"}))
print(read_file.invoke({"file_path": "sample_broken_repo/buggy_math.py"}))
print(read_file.invoke({"file_path": ".env"}))
print(search_in_repo.invoke({"folder": "sample_broken_repo", "text": "import"}))