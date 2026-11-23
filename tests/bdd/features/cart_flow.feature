Feature: Shopping cart calculations
  As a shopper
  I want to search and add products to the cart with specific quantities
  So that the cart accurately calculates line totals and the grand total

  Scenario Outline: Add products to cart and verify price calculations
    Given I am on the home page
    When I search for "<keyword>"
    And I open product "<product>"
    And I add the product to the cart with quantity <quantity>
    And I navigate to the shopping cart
    Then the cart displays product "<product>"
    And the line price matches the unit price multiplied by <quantity>
    And the cart total equals the sum of line prices

    Examples:
      | keyword | product     | quantity |
      | Pliers  | Pliers      | 2        |
      | Hammer  | Claw Hammer | 3        |
