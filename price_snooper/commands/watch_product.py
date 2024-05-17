import click

from app.product_service import ProductService


# Command Group
@click.group(name='watch-product')
def watch_product():
    """Add product to watch-list"""
    pass


@watch_product.command(name='add', help='Add product to watch list')
@click.option('--url', default=None, help='Product URL')
def install_cmd(url):
    if url is None:
        click.echo(click.style('Please provide product URL', fg='red'))
        return

    try:
        click.echo('Adding product with URL {} to watch list!!!'.format(url))
        product_service = ProductService(None)
        product_service.create_product(url)
        click.echo('Completed, Voila!!!'.format(url))
    except Exception as e:
        if e.args[0].__contains__('UNIQUE'):
            click.echo(click.style('Product already in watch list!!!', fg='red'))


@watch_product.command(name='status', help='Get products current status')
def search_cmd():
    click.echo('Show all products status')


if __name__ == '__main__':
    watch_product()
