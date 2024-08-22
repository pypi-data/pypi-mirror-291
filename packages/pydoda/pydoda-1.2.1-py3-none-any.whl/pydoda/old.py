from pydoda import Category, CustomCategory, Sentence


c = CustomCategory("x-tra", "proverbs")
print(f"c entries: {c.entries()}")
print(c.get_row("eng", "when pigs flya"))

