import collections
from decimal import Decimal, getcontext
# necessary otherwise the total amount
# will have some floating point errors
getcontext().prec = 4


class Products:
    def __init__(self):
        self._products = []

    def add_product(self, name, code, packs):
        """
        Add a new product to the products list
        """
        product = {
            'name': name,
            'code': code,
            'packs': packs
        }
        self._products.append(product)

    def _pack_to_str(self, pack):
        return ''.join(f'{pack[0]} @ ${pack[1]}')

    def print_all_products(self):
        """
        Print the full product table
        """
        # the padding for the single columns + some extra space
        len_name = max([len(p['name']) for p in self._products]) + 3
        len_code = max([len(p['code']) for p in self._products]) + 3

        print('Name'.ljust(len_name) + 'Code'.ljust(len_code) + 'Packs')

        for prod in self._products:
            first_pack = prod['packs'][0]
            line = prod['name'].ljust(len_name) + prod['code'].ljust(len_code)
            spacing = ' ' * len(line)
            line += self._pack_to_str(first_pack)
            print(line)

            for pack in prod['packs'][1:]:
                pack_str = self._pack_to_str(pack)
                print(f'{spacing}{pack_str}')

            print('')

    def _calculate_packages(self, order_num, packs):
        """
        Perform the calculation of the packaging;
        this will either return an array with the properly found
        packaging, or throw an error in case no packaging
        is possible
        """
        packs.sort(key=lambda x: x[0], reverse=True)
        package_numbers = [p[0] for p in packs]

        # all orders between [0, order_num] are calculated
        # if an order cannot be created with the given packaging
        # then -1 is used as an indication for an impossible order
        container = [[] for _ in range(order_num + 1)]
        container[0] = [0, 0, 0]
        required_packages = []
        
        # create all orders [0, order_num]
        for cur_order in range(1, order_num + 1):
            for index, pack_num in enumerate(package_numbers):
                if  cur_order >= pack_num:
                    tmp = container[cur_order-pack_num]
                    if tmp != -1:
                        container[cur_order] = [tmp[x] if x != index else tmp[x] + 1 for x in range(len(tmp))]
                        break
            else:
                container[cur_order] = -1

        if container[order_num] == -1:
            raise TypeError('Packaging not possible for this order')

        final_packages = []
        for x, y in zip(packs, container[order_num]):
            for count in range(y):
                final_packages.append(x)

        return final_packages

    def _breakdown_str(self, packaging):
        """
        Generate the breakdown string
        """
        breakdowns = []
        single_pack_numbers = [p[0] for p in packaging]

        counter = collections.Counter(single_pack_numbers)
        for pack, occurrence in counter.items():
            amount = [price[1] for price in packaging if price[0] == pack][0]
            breakdowns.append(f'{occurrence} x {pack} ${amount}')

        return breakdowns

    def _print_calculated_packaging(self, order, breakdowns, total_amount):
        """
        Prints the total value of the order and the breakdown of the price
        """
        spacing = ' ' * (len(order) + 10)
        print(f'\'{order}\' total: ${total_amount}')

        for breakdown in breakdowns:
            print(f'{spacing}{breakdown}')
        print()

    def process_order(self, order):
        """
        Process an order given by the user via the command line
        """
        parts = order.split(' ')
        # get the right product with the code from the order
        product = [prod for prod in self._products if prod['code'] == parts[1]]
        
        if len(product) == 0:
            raise TypeError('No product with that code could be found')

        # all defined packs of this product
        packs = product[0]['packs']

        # calculate the needed packages; if the order cannot be covered
        # with the predefined packaging numbers this will throw a TypeError
        packaging = self._calculate_packages(int(parts[0]), packs)

        # the total cost is the sum of all packages
        total_amount = sum([Decimal(prices[1]) for prices in packaging])

        # get the breakdown of the total price
        breakdowns = self._breakdown_str(packaging)

        # print out the results
        self._print_calculated_packaging(order, breakdowns, total_amount)


if __name__ == '__main__':
    # setup the products with predefined packaging data
    p = Products()
    p.add_product('Vegemite Scroll', 'VS5', [(3, 6.99), (5, 8.99)])
    p.add_product('Blueberry Muffin', 'MB11', [(2, 9.95), (5, 16.95), (8, 24.95)])
    p.add_product('Croissant', 'CF', [(3, 5.95), (5, 9.95), (9, 16.99)])
    p.print_all_products()

    while True:
        order = input("Please enter an order: ")
        try:
            p.process_order(order)
        except TypeError as te:
            print(f'{te}: Order \'{order}\'')
