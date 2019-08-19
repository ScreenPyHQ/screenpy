from screenpy import Target


ADD_BUTTON = Target.the("add element button").located_by("button[onclick^=addElement]")
ADDED_ELEMENTS = Target.the("added elements").located_by("button.added-manually")
