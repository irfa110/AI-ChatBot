def extract_text(content) -> str:

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for block in content:

            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):

                if block.get("type") == "text":
                    text_parts.append(
                        block.get("text", "")
                    )

        return "".join(text_parts)

    return str(content)