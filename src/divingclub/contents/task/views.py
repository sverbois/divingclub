from Products.Five.browser import BrowserView


class TaskView(BrowserView):
    """Task view"""

    def __call__(self):
        parent = self.context.__parent__
        url = parent.absolute_url()
        self.request.response.redirect(url)
