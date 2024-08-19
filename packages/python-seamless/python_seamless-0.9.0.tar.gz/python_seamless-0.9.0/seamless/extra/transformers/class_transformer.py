def class_transformer():
    def matcher(key, value):
        return key == "class_name"

    def transformer(key, class_name, element_props):
        if isinstance(class_name, list):
            class_name = " ".join(class_name)

        element_props["class"] = " ".join(str(class_name).split())
        del element_props["class_name"]

    return matcher, transformer