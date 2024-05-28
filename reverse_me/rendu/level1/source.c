int main() {
	char input[100];
	printf("Please enter key: ");
	scanf("%s", &input);
	if (strcmp(input, "__stack_check") != 0) {
		printf("Nope.\n");
	}
	else {
		printf("Good job.\n");
	}
}
