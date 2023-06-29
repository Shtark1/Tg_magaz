import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username, referer_id=None, application=0):
        with self.connection:
            if referer_id is not None:
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `username`, `referer_id`, `application`) VALUES (?, ?, ?, ?)", (user_id, username, referer_id, application,))
            else:
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `username`, `application`) VALUES (?, ?, ?)", (user_id, username, application,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def count_referer(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`id`) as count FROM `users` WHERE `referer_id` = ?", (user_id,)).fetchone()[0]

    def edit_application(self, user_id, application=1):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `application` = ? WHERE `user_id` = ?", (application, user_id,))
            self.connection.commit()

    def get_application(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `application`, `partner` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()

    def transfer_ball_user(self, user_id, count_trans, new_ref):
        with self.connection:
            all_users = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `referer_id` = ?", (user_id,)).fetchall()
            ref = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `username` = ?", (new_ref,)).fetchone()[0]

            i = 1
            for user in all_users:
                if i <= count_trans:
                    self.cursor.execute("UPDATE `users` SET `referer_id` = ? WHERE `user_id` = ?", (ref, user[0],))
                    self.connection.commit()
                else:
                    break
                i += 1
            return ref

    def accept_or_cancel_ref(self, user_id, accept_or):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `partner` = ? WHERE `user_id` = ?", (accept_or, user_id,))
            self.connection.commit()

    def get_all_data(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`").fetchall()

    def get_partners(self):
        with self.connection:
            all_part = self.cursor.execute("SELECT * FROM `users` WHERE `partner` = ?", ("True",)).fetchall()
            all_l = []
            for idx, part in enumerate(all_part):
                who_invited = self.cursor.execute("SELECT `user_id`, `username` FROM `users` WHERE `referer_id` = ?", (part[1],)).fetchall()
                all_l.append([part] + who_invited)

            return all_l

    def up_ball(self, referer_id, count_bal):
        with self.connection:
            i = 1
            while i <= count_bal:
                self.cursor.execute("INSERT INTO `users` (`username`, `referer_id`, `application`) VALUES (?, ?, ?)",
                                           ("Накрутка", referer_id, 0,))
                i += 1

    def delete_referer(self, user_id, limit):
        with self.connection:
            self.cursor.execute(
                "UPDATE `users` SET `referer_id` = NULL WHERE `referer_id` = ? AND id IN (SELECT `id` FROM `users` WHERE `referer_id` = ? LIMIT ?)",
                (user_id, user_id, limit)
            )




