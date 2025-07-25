import re
import os
import json

class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.is_available = True
    
    def to_dict(self):
        return {
            'title':self.title,
            'author':self.author,
            'is_available': self.is_available
        }
    
    @staticmethod
    def from_dict(data):
        book = Book(data.get('title','Unknown Title'),data.get('author','Unknown Author'))
        book.is_available = data.get('is_available',True)
        return book

class Member:
    def __init__(self,name,member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
    
    def to_dict(self):
        return {
            'name':self.name,
            'member_id':self.member_id,
            'borrowed_books': [book.to_dict() for book in self.borrowed_books]
        }
    
    @staticmethod
    def from_dict(data):
        member = Member(data.get('name','Unknown'),data.get('member_id','Not mentioned'))
        borrowed_books = data.get("borrowed_books",[])

        if isinstance(borrowed_books,list):
            member.borrowed_books = [Book.from_dict(book) for book in borrowed_books]
        
        else:
            member.borrowed_books = []
        
        return member

class Library:
    def __init__(self, filename='libary_data.json'):
        self.filename = filename
        self.books = []
        self.members = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename,'r') as file:
                    data = json.load(file)
                    self.books = [Book.from_dict(book_data) for book_data in data.get('books',[])]
                    self.members = [Member.from_dict(member_data) for member_data in data.get('members',[])]
            
            except json.JSONDecodeError:
                print("\nCorrupt file.Starting fresh.")
                self.books = []
                self.members = []
        
        else:
            self.books = []
            self.members = []

            with open(self.filename,'w') as file:
                json.dump({'books':[],'members':[]},file,indent=4)
    
    def save_data(self):
        try:
            with open(self.filename,'w') as file:
                data = {
                    'books':[book.to_dict() for book in self.books],
                    'members':[member.to_dict() for member in self.members]
                }

                json.dump(data,file,indent=4)

        except Exception as e:
            print(f"Error: {e}")

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
    
    @staticmethod
    def prompt_book_title():
        return input("Enter the Book Title: ").strip()
    
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
    
    def add_book(self,book_title,author):
        new_book = Book(book_title,author)
        self.books.append(new_book)
        self.save_data()
        print(f"\n✅ Book '{book_title}' by {author} added to library!\n")
    
    def add_member(self,name,member_id):
        new_member = Member(name,member_id)
        self.members.append(new_member)
        self.save_data()
        print(f"\n✅ Member '{name}' with ID {member_id} registered!\n")

    def display_books(self):
        if Library.check_none(self.books):
            print("📚 No books in the library yet.\n")
            return

        print("📚 All Books in Library:\n")
        for book in self.books:
            print(f"Book: {book.title}")
            print(f"Author: {book.author}")
            print("Book is Available\n" if book.is_available else "Book is Unavailable\n")
        
        print(f"Total Books: {len(self.books)} \n")
    
    def display_members(self):
        if Library.check_none(self.members):
            print("No members registered yet.")
            return
        
        print(f"Library Members: \n")
        for member in self.members:
            print(f"Name: {member.name} | Member_id: {member.member_id}\n")

        print(f"Total members: {len(self.members)}\n")
    
    def issue_book(self,member_id,book_title):
        member = self.get_member(member_id)
        if Library.check_none(member):
            print("❌ Member not found!\n")
            return

        book = self.get_book(book_title)
        
        if Library.check_none(book):
            print("❌ Book not found!\n")
            return
        
        if not book.is_available:
            print(f"❌ '{book.title}' is currently unavailable.\n")
        
        book.is_available = False
        member.borrowed_books.append(book)
        self.save_data()
        print(f"✅ '{book.title}' issued to {member.name}\n")
    
    def return_book(self,member_id,book_title):
        member = self.get_member(member_id)
        if Library.check_none(member):
            print("❌ Member not found!\n")
            return
        
        book = None

        for b in member.borrowed_books:
            if b.title == book_title:
                book = b
                break
        
        if Library.check_none(book):
            print("❌ This book was not borrowed by the member!\n")
            return
    
        book.is_available = True
        member.borrowed_books.remove(book)
        self.save_data()
        print(f"✅ '{book.title}' issued by '{member.name}' is returned to library and '{book.title}' is available in library!\n")

    def view_borrowed_books(self,member_id):
        member = self.get_member(member_id)
        
        if Library.check_none(member):
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
    
    def print_library_summary(self):
        print("📚 Library Summary:")
        print(f"• Total Books: {len(self.books)}")
        print(f"• Total Members: {len(self.members)}")

        issued_books = sum(1 for book in self.books if not book.is_available)
        print(f"• Currently Issued Books: {issued_books}")

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

        try:
            user_choice = int(input("Enter your choice: "))

        except ValueError:
            print("Error: Please enter a valid input!")
        
        else:
            match user_choice:
                case 1:
                    book_title = my_library.prompt_book_title()
                    author = input("Enter author name of the book: ").strip()

                    my_library.add_book(book_title,author)
                
                case 2:
                    name = input("Enter the name to register in member list: ").strip()
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

                    book_title = my_library.prompt_book_title()

                    my_library.issue_book(member_id,book_title)
                
                case 4:
                    member_id = my_library.prompt_member_id()
                    if Library.check_none(member_id):
                        print("Invalid Member id.")
                        continue

                    book_title = my_library.prompt_book_title()
                    
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
                    query = input("Enter the book to search: ").strip()
                    my_library.search_book(query)

                case 9:
                    my_library.print_library_summary()
                    print("\n🙏 Thank you for using our Library System!\n")
                    break
                
                case _:
                    print("Invalid! Please enter valid number between 1 to 9")