from .ask_prompts import AskPrompts
from .base_coder import Coder
from .editblock_coder import find_original_update_blocks


class AskCoder(Coder):
    """Ask questions about code without making any changes."""

    edit_format = "ask"
    gpt_prompts = AskPrompts()

    def get_edits(self, **kwargs):
        content = self.partial_response_content

        # might raise ValueError for malformed ORIG/UPD blocks
        edits = list(find_original_update_blocks(content, self.fence, valid_fnames=self.get_inchat_relative_files()))
        print(edits)

        self.shell_commands += [edit[1] for edit in edits if edit[0] is None]
        edits = [edit for edit in edits if edit[0] is not None]

        if edits:
            self.io.tool_error("ask mode does not support code edits")
        return []
