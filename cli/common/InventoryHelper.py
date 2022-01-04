class InventoryHelper:

    lines = []

    def add_group(self, group_name: str, content: []):
        self.lines.append(f'[{group_name}]')

        [self.lines.append(i) for i in content]

    def generate_inventory_file(self, output_file: str):
        inventory_file = open(output_file, "w")
        [inventory_file.write(f'{i}\n') for i in self.lines]
        inventory_file.close()
