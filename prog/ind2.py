#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys

from dotenv import dotenv_values


def add_product(staff, name, post, year):
    """
    Добавить данные о работнике.
    """
    staff.append({"name": name, "market": post, "count": year})
    return staff


def display_products(workers):
    """
    Отобразить список работников.
    """
    if workers:
        line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 10)
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^10} |".format(
                "№", "Название продукта", "Имя магазина", "Стоимость"
            )
        )
        print(line)
        for idx, worker in enumerate(workers, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>10} |".format(
                    idx,
                    worker.get("name", ""),
                    worker.get("market", ""),
                    worker.get("count", 0),
                )
            )
        print(line)

    else:
        print("Список продуктов пуст.")


def select_products(products, find_name):
    """
    Выбрать продукт с заданным именем.
    """
    result = []
    for product in products:
        if product.get("name_of_product") == find_name:
            result.append(product)

    return result


def save_products(file_name, staff):
    """
    Сохранить всех работников в JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fount:
        json.dump(staff, fount, ensure_ascii=False, indent=4)


def load_products(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    """
    Главная функция программы.
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d", "--data", action="store", required=False, help="The data file name"
    )

    parser = argparse.ArgumentParser("products")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new product")
    add.add_argument(
        "-n", "--name", action="store", required=True, help="The product's name"
    )
    add.add_argument("-m", "--market", action="store", help="The market's name")
    add.add_argument(
        "-c", "--count", action="store", type=int, required=True, help="The count"
    )

    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all products"
    )

    info = subparsers.add_parser(
        "info", parents=[file_parser], help="Select the products"
    )

    info.add_argument(
        "-p",
        "--name_product",
        action="store",
        type=str,
        required=True,
        help="The required name of product",
    )

    args = parser.parse_args()
    data_file = args.data
    if not data_file:
        data_file = dotenv_values(".env")["PRODUCTS_DATA"]
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        products = load_products(data_file)
    else:
        products = []

    if args.command == "add":
        products = add_product(products, args.name, args.market, args.count)
        is_dirty = True

    elif args.command == "display":
        display_products(products)

    elif args.command == "info":
        selected = select_products(products, args.name_product)
        display_products(selected)

    if is_dirty:
        save_products(data_file, products)


if __name__ == "__main__":
    main()
