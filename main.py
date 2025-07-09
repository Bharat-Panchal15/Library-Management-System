import re

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.is_available = True

class Member:
    def __init__(self,name,member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

class Library:
    def __init__(self):
        self.books = []
        self.members = []

    @staticmethod
    def check_none(val):
        if val is None:
            return True
        return False
    
    @staticmethod
    def prompt_member_id():
        id_pattern = re.compile(r"^\d{4}$")
        member_id = input("Enter member ID (e.g. 1001): ")

        if not member_id.isdigit():
            print("Invalid member id. It must only contain numbers.")
            return None

        if bool(id_pattern.match(member_id)):
            return int(member_id)
        return None
    
    def get_member(self,member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def get_book(self,book_title):
        for book in self.books:
            if book.title == book_title:
                return book
        
        return None
    
    def add_book(self,title,author):
        new_book = Book(title,author)
        self.books.append(new_book)
        print(f"\n✅ Book '{title}' by {author} added to library!\n")
    
    def add_member(self,name,member_id):
        new_member = Member(name,member_id)
        self.members.append(new_member)
        print(f"\n✅ Member '{name}' with ID {member_id} registered!\n")

    def display_books(self):
        if not self.books:
            print("📚 No books in the library yet.\n")
            return

        print("📚 All Books in Library:\n")
        for book in self.books:
            print(f"Book: {book.title}")
            print(f"Author: {book.author}")
            print("Book is Available\n" if book.is_available else "Book is Unavailable\n")
        
        print(f"Total Books: {len(self.books)} \n")
    
    def display_members(self):
        if not self.members:
            print("No members registered yet.")
            return
        
        print(f"Library Members: \n")
        for member in self.members:
            print(f"Name: {member.name} | Member_id: {member.member_id}\n")

        print(f"Total members: {len(self.members)}\n")
    
    def issue_book(self,member_id,book_title):
        member = self.get_member(member_id)
        
        if member is None:
            print("❌ Member not found!\n")
            return

        book = self.get_book(book_title)
        
        if book is None:
            print("❌ Book not found!\n")
            return
        
        if not book.is_available:
            print(f"❌ '{book.title}' is currently unavailable.\n")
        
        book.is_available = False
        member.borrowed_books.append(book)
        print(f"✅ '{book.title}' issued to {member.name}\n")
    
    def return_book(self,member_id,book_title):
        member = self.get_member(member_id)
        
        if member is None:
            print("❌ Member not found!\n")
            return
        
        book = None

        for b in member.borrowed_books:
            if b.title == book_title:
                book = b
                break
        
        if book is None:
            print("❌ This book was not borrowed by the member!\n")
            return
    
        book.is_available = True
        member.borrowed_books.remove(book)
        print(f"✅ '{book.title}' issued by '{member.name}' is returned to library and '{book.title}' is available in library!\n")

    def view_borrowed_books(self,member_id):
        member = self.get_member(member_id)
        
        if member is None:
            print("❌ Member not found!\n")
            return
        
        if not member.borrowed_books:
            print(f"❌ No book borrowed by {member.name}!\n")
            return

        print(f"These are the books borrowed by {member.name}\n")
        for idx,book in enumerate(member.borrowed_books,start=1):
            print(f"{idx}. {book.title} by {book.author}")
    
    def search_book(self,query):
        found = False
        for book in self.books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                print(f"{book.title} by {book.author} - {'Available' if book.is_available else 'Not available'}\n")
                
                found = True
        
        if not found:
            print("❌ No books found matching your choice.\n")
            return

if __name__ == "__main__":
    my_library = Library()

    while True:
        print("[1] Add Book")
        print("[2] Add Member")
        print("[3] Issue Book")
        print("[4] Return Book")
        print("[5] View all Books")
        print("[6] View all Members")
        print("[7] View borrowed books")
        print("[8] Search Book")
        print("[9] Exit\n")

        user_choice = int(input("Enter your choice: "))

        match user_choice:
            case 1:
                title = input("Enter the title of the book you want to add: ")
                author = input("Enter author name of the book: ")

                my_library.add_book(title,author)
            
            case 2:
                name = input("Enter the name to register in member list: ")
                member_id = my_library.prompt_member_id()

                if Library.check_none(member_id):
                    print("Please enter valid id.")
                    continue

                my_library.add_member(name,member_id)
            
            case 3:
                member_id = my_library.prompt_member_id()
                if Library.check_none(member_id):
                    print("Invalid Member id.")
                    continue

                book_title = input("Enter title of the book to issue: ")

                my_library.issue_book(member_id,book_title)
            
            case 4:
                member_id = my_library.prompt_member_id()
                if Library.check_none(member_id):
                    print("Invalid Member id.")
                    continue

                book_title = input("Enter title of the book to return which book: ")
                
                my_library.return_book(member_id,book_title)
            
            case 5:
                my_library.display_books()
            
            case 6:
                my_library.display_members()
            
            case 7:
                member_id = my_library.prompt_member_id()
                if Library.check_none(member_id):
                    print("Invalid Member id.")
                    continue

                my_library.view_borrowed_books(member_id)
            
            case 8:
                query = input("Enter the book to search: ")
                my_library.search_book(query)

            case 9:
                print("📚 Library Summary:")
                print(f"• Total Books: {len(my_library.books)}")
                print(f"• Total Members: {len(my_library.members)}")

                issued_books = sum(1 for book in my_library.books if not book.is_available)
                print(f"• Currently Issued Books: {issued_books}")
                print("\n🙏 Thank you for using our Library System!\n")
                break
            
            case _:
                print("Invalid! Please enter valid")