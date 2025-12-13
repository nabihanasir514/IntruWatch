#include<iostream>
using namespace std;
//making a linked list of usernames and passwords
class Node{
	public:
	string username;
	string password;
	string designation;
	char gender;
	Node *next;
	
	Node(string n, string pass, string des, char gen){
		
		username = n;
		password = pass;
		next = NULL;
		designation = des;
		gender = gen;
	}
};

class student{
	
	int reg_no;
	string room_no;
	public:
	student(int reg, string room){
		reg_no = reg;
		room_no = room;
	}
};

class faculty{
	
	int employee_no;
	public:
	faculty(int emp_no){
		employee_no = emp_no;
	}
};

Node *head = NULL;
//function to insert usernames and passwords into said linked list
void Register (string name, string password, string designation, char gender ){
    Node *newnode = new Node(name, password, designation, gender);
	if(designation == "student"){
		int reg;
		string room;
		cout<<"Enter registeration number: ";
		cin>>reg;
		cout<<endl;
		cout<<"Enter room number: ";
		cin>>room;
    	student s(reg, room);
	}
	
	else if(designation == "faculty"){
		int emp_no;
		cout<<"Enter employee number: ";
		cin>>emp_no;
		faculty f(emp_no);
	}
	newnode->next = head;
	head = newnode;	
}



//function to match user details to values already in the server
bool sign_in(string n, string pass, string des, char gen){
	Node* temp = head;
	if(pass == temp->password && n == temp->username && des == temp->designation){
		return true;
		temp = temp->next;
	}
	
	return false;
}
//function to sign in
void sign_up(string n, string pass, string des, char gen){
	Register(n, pass, des, gen);
	
}



int main(){
	
    
	sign_up("Muhammad", "890", "student", 'M');
	
	cout<<sign_in("Muhammad", "890", "student", 'M');
	
	
	
}