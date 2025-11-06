import wx
from db import Database
from decimal import Decimal

class GameDBApp(wx.App):
    def OnInit(self):
        self.db = Database()
        self.frame = MainFrame(None, title="Game Review Database")
        self.frame.Show()
        return True

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        self.db = wx.GetApp().db
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="Game Review Database")
        title.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(title, flag=wx.ALL|wx.CENTER, border=10)

        # Buttons
        buttons = [
            ("Add User", self.on_add_user),
            ("Add Game", self.on_add_game),
            ("Add Review", self.on_add_review),
            ("Search Games by Tag", self.on_search_by_tag),
            ("View Users", self.on_view_users),
            ("View Games", self.on_view_games),
            ("View Reviews", self.on_view_reviews),
            ("View Games by Average Rating", self.on_view_games_by_rating)
        ]

        for label, handler in buttons:
            btn = wx.Button(panel, label=label)
            btn.Bind(wx.EVT_BUTTON, handler)
            vbox.Add(btn, flag=wx.ALL|wx.EXPAND, border=5)

        panel.SetSizer(vbox)

    def on_add_user(self, event):
        dialog = AddUserDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def on_add_game(self, event):
        dialog = AddGameDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def on_add_review(self, event):
        dialog = AddReviewDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def on_search_by_tag(self, event):
        dialog = SearchByTagDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def on_view_users(self, event):
        users = self.db.get_users()
        self.show_list("Users", ["User ID", "Username", "Gender", "Age"], users)

    def on_view_games(self, event):
        games = self.db.get_games()
        self.show_list("Games", ["Game ID", "Title", "Developer", "Tags"], games)

    def on_view_reviews(self, event):
        reviews = self.db.get_reviews()
        self.show_list("Reviews", ["Review ID", "User ID", "Game Title", "Rating", "Added Date"], reviews, data_columns=[0,1,2,3,5])

    def on_view_games_by_rating(self, event):
        games = self.db.get_games_average_rating()
        self.show_list("Games by Average Rating", ["Game ID", "Title", "Developer", "Average Rating"], games)

    def show_list(self, title, columns, data, data_columns=None):
        dialog = wx.Dialog(self, title=title, size=(600, 400))
        panel = wx.Panel(dialog)
        vbox = wx.BoxSizer(wx.VERTICAL)

        list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        for i, col in enumerate(columns):
            list_ctrl.InsertColumn(i, col)

        display_data = data
        if data_columns:
            display_data = [tuple(row[i] for i in data_columns) for row in data]

        for item in display_data:
            index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), str(item[0]))
            for i in range(1, len(item)):
                value = item[i]
                col_name = columns[i] if i < len(columns) else ""
                if (isinstance(value, float) or isinstance(value, Decimal)) and ("Rating" in col_name or "Average" in col_name):
                    value = f"{float(value):.1f}" if value is not None else "N/A"
                else:
                    value = str(value) if value is not None else ""
                list_ctrl.SetItem(index, i, value)

        # Check if this is Reviews list and add double-click handler
        if "Reviews" in title:
            list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda e: self.on_comment_double_click(e, data))

        # Check if this is Games list and add double-click handler
        if title.startswith("Games"):
            list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda e: self.on_game_double_click(e, data))

        vbox.Add(list_ctrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)

        close_btn = wx.Button(panel, label="Close")
        close_btn.Bind(wx.EVT_BUTTON, lambda e: dialog.EndModal(wx.ID_OK))
        vbox.Add(close_btn, flag=wx.ALL|wx.CENTER, border=10)

        panel.SetSizer(vbox)
        dialog.ShowModal()
        dialog.Destroy()

    def on_game_double_click(self, event, data):
        item_index = event.GetIndex()
        if item_index >= 0 and item_index < len(data):
            game_id = str(data[item_index][0])  # Game ID is at index 0
            game_title = str(data[item_index][1])  # Game title is at index 1

            # Get all reviews for this game
            reviews = self.db.get_reviews_by_game(game_id)
            if reviews:
                self.show_list(f"Reviews for {game_title}", ["Review ID", "User ID", "Rating", "Added Date"], reviews, data_columns=[0,1,2,4])
            else:
                wx.MessageBox(f"No reviews found for {game_title}.", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_comment_double_click(self, event, data):
        item_index = event.GetIndex()
        if item_index >= 0 and item_index < len(data):
            if len(data[item_index]) == 6:  # Full reviews: review_id, user_id, game_title, rating, comment, added_date
                review_id, user_id, game_title, rating, comment, added_date = data[item_index]
            else:  # Game reviews: review_id, username, rating, comment, added_date
                review_id, username, rating, comment, added_date = data[item_index]
                game_title = "this game"  # We don't have game title in this context
                user_id = username  # Use username instead

            comment_dialog = wx.Dialog(self, title=f"Review Details (ID: {review_id})", size=(400, 300))
            panel = wx.Panel(comment_dialog)
            vbox = wx.BoxSizer(wx.VERTICAL)

            # Display game title (if available)
            if game_title != "this game":
                game_label = wx.StaticText(panel, label=f"Game: {game_title}")
                game_label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                vbox.Add(game_label, flag=wx.ALL, border=10)

            # Display user
            user_label = wx.StaticText(panel, label=f"User: {user_id}")
            vbox.Add(user_label, flag=wx.ALL, border=10)

            # Display rating
            rating_label = wx.StaticText(panel, label=f"Rating: {rating}/5")
            vbox.Add(rating_label, flag=wx.ALL, border=10)

            # Display comment
            comment_label = wx.StaticText(panel, label="Comment:")
            vbox.Add(comment_label, flag=wx.ALL, border=5)
            text_ctrl = wx.TextCtrl(panel, value=str(comment), style=wx.TE_MULTILINE | wx.TE_READONLY)
            vbox.Add(text_ctrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)

            close_btn = wx.Button(panel, label="Close")
            close_btn.Bind(wx.EVT_BUTTON, lambda e: comment_dialog.EndModal(wx.ID_OK))
            vbox.Add(close_btn, flag=wx.ALL|wx.CENTER, border=10)

            panel.SetSizer(vbox)
            comment_dialog.ShowModal()
            comment_dialog.Destroy()

class AddUserDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddUserDialog, self).__init__(parent, title="Add User", size=(300, 250))
        self.db = parent.db
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.user_id = wx.TextCtrl(panel)
        self.username = wx.TextCtrl(panel)
        self.gender = wx.Choice(panel, choices=["男", "女"])
        self.age = wx.TextCtrl(panel)

        fields = [
            ("User ID:", self.user_id),
            ("Username:", self.username),
            ("Gender:", self.gender),
            ("Age:", self.age)
        ]

        for label, ctrl in fields:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(panel, label=label), flag=wx.RIGHT, border=5)
            hbox.Add(ctrl, proportion=1)
            vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, label="OK")
        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_btn = wx.Button(panel, label="Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))
        btn_box.Add(ok_btn)
        btn_box.Add(cancel_btn, flag=wx.LEFT, border=5)
        vbox.Add(btn_box, flag=wx.ALL|wx.CENTER, border=10)

        panel.SetSizer(vbox)

    def on_ok(self, event):
        try:
            user_id = self.user_id.GetValue()
            username = self.username.GetValue()
            gender = self.gender.GetStringSelection()
            age = int(self.age.GetValue())
            self.db.add_user(user_id, username, gender, age)
            wx.MessageBox("User added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

class AddGameDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddGameDialog, self).__init__(parent, title="Add Game", size=(400, 400))
        self.db = parent.db
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.game_id = wx.TextCtrl(panel)
        self.title = wx.TextCtrl(panel)
        self.developer = wx.TextCtrl(panel)

        fields = [
            ("Game ID:", self.game_id),
            ("Title:", self.title),
            ("Developer:", self.developer)
        ]

        for label, ctrl in fields:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(panel, label=label), flag=wx.RIGHT, border=5)
            hbox.Add(ctrl, proportion=1)
            vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        # Tags selection
        tags = [tag[1] for tag in self.db.get_tags()]
        self.tag_checklist = wx.CheckListBox(panel, choices=tags)
        tag_hbox = wx.BoxSizer(wx.HORIZONTAL)
        tag_hbox.Add(wx.StaticText(panel, label="Tags:"), flag=wx.RIGHT, border=5)
        tag_hbox.Add(self.tag_checklist, proportion=1)
        add_tag_btn = wx.Button(panel, label="Add New Tag")
        add_tag_btn.Bind(wx.EVT_BUTTON, self.on_add_tag)
        tag_hbox.Add(add_tag_btn, flag=wx.LEFT, border=5)
        vbox.Add(tag_hbox, flag=wx.ALL|wx.EXPAND, border=5)

        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, label="OK")
        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_btn = wx.Button(panel, label="Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))
        btn_box.Add(ok_btn)
        btn_box.Add(cancel_btn, flag=wx.LEFT, border=5)
        vbox.Add(btn_box, flag=wx.ALL|wx.CENTER, border=10)

        panel.SetSizer(vbox)

    def on_add_tag(self, event):
        dialog = wx.TextEntryDialog(self, "Enter new tag name:", "Add New Tag")
        if dialog.ShowModal() == wx.ID_OK:
            new_tag = dialog.GetValue()
            if new_tag:
                try:
                    self.db.add_tag(new_tag)
                    self.tag_checklist.Append(new_tag)
                    wx.MessageBox("Tag added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        dialog.Destroy()

    def on_ok(self, event):
        game_id = self.game_id.GetValue().strip()
        title = self.title.GetValue().strip()
        developer = self.developer.GetValue().strip()
        selected_indices = self.tag_checklist.GetCheckedItems()
        tag_names = [self.tag_checklist.GetString(i) for i in selected_indices]

        if not game_id or not title:
            wx.MessageBox("Game ID and Title are required!", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            self.db.add_game(game_id, title, developer, tag_names)
            wx.MessageBox("Game added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

class AddReviewDialog(wx.Dialog):
    def __init__(self, parent):
        super(AddReviewDialog, self).__init__(parent, title="Add Review", size=(300, 300))
        self.db = parent.db
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.user_id = wx.TextCtrl(panel)
        self.game_id = wx.TextCtrl(panel)
        self.rating = wx.Choice(panel, choices=["1", "2", "3", "4", "5"])
        self.comment = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fields = [
            ("User ID:", self.user_id),
            ("Game ID:", self.game_id),
            ("Rating:", self.rating),
            ("Comment:", self.comment)
        ]

        for label, ctrl in fields:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(panel, label=label), flag=wx.RIGHT, border=5)
            if ctrl == self.comment:
                vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)
                vbox.Add(ctrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
            else:
                hbox.Add(ctrl, proportion=1)
                vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, label="OK")
        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_btn = wx.Button(panel, label="Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))
        btn_box.Add(ok_btn)
        btn_box.Add(cancel_btn, flag=wx.LEFT, border=5)
        vbox.Add(btn_box, flag=wx.ALL|wx.CENTER, border=10)

        panel.SetSizer(vbox)

    def on_ok(self, event):
        try:
            user_id = self.user_id.GetValue()
            game_id = self.game_id.GetValue()
            rating = int(self.rating.GetStringSelection())
            comment = self.comment.GetValue()
            self.db.add_review(user_id, game_id, rating, comment)
            wx.MessageBox("Review added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

class SearchByTagDialog(wx.Dialog):
    def __init__(self, parent):
        super(SearchByTagDialog, self).__init__(parent, title="Search Games by Tag", size=(300, 150))
        self.db = parent.db
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        tags = [tag[1] for tag in self.db.get_tags()]
        self.tag_choice = wx.Choice(panel, choices=tags)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(panel, label="Tag:"), flag=wx.RIGHT, border=5)
        hbox.Add(self.tag_choice, proportion=1)
        vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        search_btn = wx.Button(panel, label="Search")
        search_btn.Bind(wx.EVT_BUTTON, self.on_search)
        cancel_btn = wx.Button(panel, label="Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CANCEL))
        btn_box.Add(search_btn)
        btn_box.Add(cancel_btn, flag=wx.LEFT, border=5)
        vbox.Add(btn_box, flag=wx.ALL|wx.CENTER, border=10)

        panel.SetSizer(vbox)

    def on_search(self, event):
        tag_name = self.tag_choice.GetStringSelection()
        if tag_name:
            games = self.db.get_games_by_tag(tag_name)
            if games:
                self.GetParent().show_list(f"Games with tag '{tag_name}'", ["Game ID", "Title", "Developer", "Average Rating"], games)
            else:
                wx.MessageBox("No games found with this tag.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Please select a tag.", "Info", wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = GameDBApp()
    app.MainLoop()
