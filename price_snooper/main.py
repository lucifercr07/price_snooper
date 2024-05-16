from app.product_service import ProductService
import click


class CommandWithOptionalPassword(click.Command):
    def parse_args(self, ctx, args):
        for i, a in enumerate(args):
            if args[i] == '--passwd':
                try:
                    passwd = args[i + 1] if not args[i + 1].startswith('--') else None
                except IndexError:
                    passwd = None
                if not passwd:
                    passwd = click.prompt('Password', hide_input=True)
                    args.insert(i + 1, passwd)
        return super(CommandWithOptionalPassword, self).parse_args(ctx, args)


@click.command(cls=CommandWithOptionalPassword)
@click.option('--watch_product', default=None, help='Add product to watchlist')
@click.option('--current_product_status', default=None,
              help='Get current status of product (Whether to buy or not, price etc.)')
def main(watch_product, current_product_status):
    click.secho('Welcome.....', fg='green', bold=True)
    if watch_product:
        click.secho('Getting you new pass...', fg='green', bold=True)
    elif current_product_status:
        product_service = ProductService(None)
        product_service.create_product('https://amzn.in/d/82OFVrw')
    else:
        click.secho('Usage: price_snooper.py --help', fg="red", bold=True)


if __name__ == '__main__':
    main()
