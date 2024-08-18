# MIT License
#
# Copyright (c) 2022 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .client import Client


class Labeler:

    @staticmethod
    def label(title, body, labels=[], model_name="gpt-4", temperature=0, callbacks=[]):
        """
        Label a GitHub issue based on its title and body.
        """
        prompt = f"""
        Given the following GitHub issue, assign the most appropriate label(s) from this list:
        {', '.join(labels)}

        Issue Title: {title}
        Issue Body: {body}

        Return only the label(s) that best fit the issue, separated by commas if multiple labels apply.
        """

        chain = Client.create_chat_chain(
            model_name,
            temperature,
            [
                ("system", "You are an AI assistant that labels GitHub issues accurately."),
                ("user", prompt),
            ],
            callbacks,
        )

        response = chain.invoke({"title": title, "body": body})

        return [label.strip() for label in response.split(',')]
