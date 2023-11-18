// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public funderRecord;
    address[] public funderList;
    //address btcUsdFeed;
    address ethUsdFeed;
    address public owner;
    AggregatorV3Interface public priceFeed;
    uint256 minUSD;

    constructor(address _priceFeed) {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
        ethUsdFeed = 0x694AA1769357215DE4FAC081bf1f309aDC325306;
        //address btcUsdFeed = 0x1b44F3514812d835EB1BDB0acB33d3fA3351Ee43;
        minUSD = 10;
    }

    function fund() public payable {
        require(
            getConversionRate(msg.value) > minUSD,
            "minimum value 10 USD required"
        );
        funderRecord[msg.sender] += msg.value;
        funderList.push(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function getMinUsd() public view returns (uint256) {
        return minUSD;
    }

    function withdrawFull() public payable onlyOwner {
        uint256 withAmount = address(this).balance;
        payable(msg.sender).transfer(withAmount);

        for (
            uint256 funderIndex = 0;
            funderIndex < funderList.length;
            funderIndex++
        ) {
            address funder = funderList[funderIndex];
            funderRecord[funder] = 0;
        }

        funderList = new address[](0);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint) {
        (
            ,
            /*uint80 roundID*/ int answer /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/,
            ,
            ,

        ) = priceFeed.latestRoundData(); // returns 8 decimal places

        return uint(answer);
    }

    function getConversionRate(
        uint256 _ethAmountInWei
    ) public view returns (uint256) {
        uint toUsdRate = 10 ** (18 + 8); //
        uint ethPrice = getPrice();
        uint256 usdAmount = (ethPrice * _ethAmountInWei) / toUsdRate;
        return usdAmount;
    }

    function usdToWei(uint256 _usdAmount) public view returns (uint256) {
        return (_usdAmount * (10 ** 26)) / getPrice();
    }
}
