# optlib
A library to price financial options using closed-form solutions written in Python. Original code written by Davis Edwards, packaged by Daniel Rojas. MIT License.

## Includes
1. European Options: Black-Scholes, Black76, Merton, Garman-Kohlhagan;
2. Spread Options: Kirk's Approximation, Heat Rate Options;
3. American Options: Bjerksund-Stensland
4. Implied Volatility
5. Asian Options

## Installation


# Closed Form Option Pricing Formulas
## Generalized Black Scholes (GBS) and similar models

**Changelog**

* 1/1/2017 Davis Edwards, Created GBS and Asian option formulas
* 3/2/2017 Davis Edwards, added TeX formulas to describe calculations
* 4/9/2017 Davis Edwards, added spread option (Kirk's approximation)
* 5/10/2017 Davis Edwards, added graphics for sensitivity analysis
* 5/18/2017 Davis Edwards, added Bjerksund-Stensland (2002) approximation for American Options
* 5/19/2017 Davis Edwards, added implied volatility calculations
* 6/7/2017 Davis Edwards, expanded sensitivity tests for American option approximation.
* 6/21/2017 Davis Edwards, added documentation for Bjerksund-Stensland models
* 7/21/2017 Davis Edwards, refactored all of the functions to match the parameter order to Haug's "The Complete Guide to Option Pricing Formulas".

**TODO List**

1. Since the Asian Option valuation uses an approximation, need to determine the range of acceptable stresses that can be applied to the volatility input
2. Sub-class the custom assertions in this module to work with "unittest"
3. Update the greek calculations for American Options - currently the Greeks are approximated by the greeks from GBS model.
4. Add a bibliography referencing the academic papers used as sources
5. Finish writing documentation formulas for Close-Form approximation for American Options
6. Refactor the order of parameters for the function calls to replicate the order of parameters in academic literature
7. Add figures to README.md

## Purpose

The software in this model is intended to price particular types of financial products called "options". These are a common type of financial product and fall into the category of "financial derivative". This documentation assumes that the reader is already familiar with options terminology. The models are largely variations of the Black Scholes Merton option framework (collectively called "Black Scholes Genre" or "Generalized Black Scholes") that are used to price European options (options that can only be exercised at one point in time). This library also includes approximations to value American options (options that can be exercised prior to the expiration date) and implied volatility calculators.

Pricing Formulas
1. `black_scholes()` Stock Options (no dividend yield)
2. `merton()` Assets with continuous dividend yield (Index Options)
3. `black_76()` Commodity Options
4. `garman_kohlhagen()` FX Options
5. `asian_76()` Asian Options on Commodities
6. `kirks_76()` Spread Options (Kirk's Approximation)
7. `american()` American options
8. `american_76()` American Commodity Options

Implied Volatility Formulas
9.  `euro_implied_vol()` Implied volatility calculator for European options
10.  `euro_implied_vol_76()` Implied volatility calculator for European commodity options
11.  `amer_implied_vol()` Implied volatility calculator for American options
12.  `amer_implied_vol_76()` Implied volatility calculator for American commodity options

Note:
In honor of the `black_76` model, the `_76` on the end of functions indicates a commodity option.

## Scope
This model is built to price financial option contracts on a wide variety of financial commodities. These options are widely used and represent the benchmark to which other (more complicated) models are compared. While those more complicated models may outperform these models in specific areas, out-performance is relatively uncommon. By an large, these models have taken on all challengers and remain the de-facto industry standard.

## Theory

### Generalized Black Scholes
Black Scholes genre option models widely used to value European options. The original “Black Scholes” model was published in 1973 for non-dividend paying stocks. This created a revolution in quantitative finance and opened up option trading to the general population. Since that time, a wide variety of extensions to the original Black Scholes model have been created. Collectively, these are referred to as "Black Scholes genre” option models. Modifications of the formula are used to price other financial instruments like dividend paying stocks, commodity futures, and FX forwards. Mathematically, these formulas are nearly identical. The primary difference between these models is whether the asset has a carrying cost (if the asset has a cost or benefit associated with holding it) and how the asset gets present valued. To illustrate this relationship, a “generalized” form of the Black Scholes equation is shown below.

The Black Scholes model is based on number of assumptions about how financial markets operate. Black Scholes style models assume:

1.	**Arbitrage Free Markets**. Black Scholes formulas assume that traders try to maximize their personal profits and don’t allow arbitrage opportunities (riskless opportunities to make a profit) to persist.
2.	**Frictionless, Continuous Markets**. This assumption of frictionless markets assumes that it is possible to buy and sell any amount of the underlying at any time without transaction costs.
3.	**Risk Free Rates**. It is possible to borrow and lend money at a risk-free interest rate
4.	**Log-normally Distributed Price Movements**. Prices are log-normally distributed and described by Geometric Brownian Motion
5.	**Constant Volatility**. The Black Scholes genre options formulas assume that volatility is constant across the life of the option contract.

In practice, these assumptions are not particularly limiting. The primary limitation imposed by these models is that it is possible to (reasonably) describe the dispersion of prices at some point in the future in a mathematical equation.

In the traditional Black Scholes model intended to price stock options, the underlying assumption is that the stock is traded at its present value and that prices will follow a random walk diffusion style process over time. Prices are assumed to start at the spot price and, on the average, to drift upwards over time at the risk free rate. The Merton formula modifies the basic Black Scholes equation by introducing an additional term to incorporate dividends or holding costs. The Black 76 formula modifies the assumption so that the underlying starts at some forward price rather than a spot price. A fourth variation, the Garman Kohlhagen model, is used to value foreign exchange (FX) options. In the GK model, each currency in the currency pair is discounted based on its own interest rate.

1. **Black Scholes (Stocks)**. In the traditional Black Scholes model, the option is based on common stock - an instrument that is traded at its present value. The stock price does not get present valued – it starts at its present value (a ‘spot price’) and drifts upwards over time at the risk free rate.
2. **Merton (Stocks with continuous dividend yield)**. The Merton model is a variation of the Black Scholes model for assets that pay dividends to shareholders. Dividends reduce the value of the option because the option owner does not own the right to dividends until the option is exercised.
3. **Black 76 (Commodity Futures)**. The Black 76 model is for an option where the underlying commodity is traded based on a future price rather than a spot price. Instead of dealing with a spot price that drifts upwards at the risk free rate, this model deals with a forward price that needs to be present valued.
4. **Garman-Kohlhagen (FX Futures)**. The Garman Kohlhagen model is used to value foreign exchange (FX) options. In the GK model, each currency in the currency pair is discounted based on its own interest rate.

An important concept of Black Scholes models is that the actual way that the underlying asset drifts over time isn't important to the valuation. Since European options can only be exercised when the contract expires, it is only the distribution of possible prices on that date that matters - the path that the underlying took to that point doesn't affect the value of the option. This is why the primary limitation of the model is being able to describe the dispersion of prices at some point in the future, not that the dispersion process is simplistic.

The generalized Black Scholes formula can found below (see Figure 1). While these formulas may look complicated at first glance, most of the terms can be found as part of an options contract or are prices readily available in the market.  The only term that is difficult to calculate is the implied volatility (σ). Implied volatility is typically calculated using prices of other options that have recently been traded.

*Call Price*

$$
\begin{equation}
C = Fe^{(b-r)T} N(D_1) - Xe^{-rT} N(D_2)
\end{equation}
$$

*Put Price*

$$
\begin{equation}
P = Xe^{-rT} N(-D_2) - Fe^{(b-r)T} N(-D_1)
\end{equation}
$$

with the following intermediate calculations

$$
\begin{equation}
D_1 = \frac{ln\frac{F}{X} + (b+\frac{V^2}{2})T}{V*\sqrt{T}}
\end{equation}
$$

$$
\begin{equation}
D_2 = D_1 - V\sqrt{T}
\end{equation}
$$

and the following inputs

|    Symbol    |    Meaning    |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    F or S   |    **Underlying Price**. The price of the underlying asset on the valuation date. S is used commonly used to represent a spot price, F a forward price     |
|    X    |    **Strike Price**. The strike, or exercise, price of the option.    |
|    T    |    **Time to expiration**. The time to expiration in years. This can be calculated by comparing the time between the expiration date and the valuation date. T = (t_1 - t_0) / 365    |
|    t_0    |    **Valuation Date**. The date on which the option is being valued. For example, it might be today’s date if the option we being valued today.    |
|    t_1    |    **Expiration Date**. The date on which the option must be exercised.    |
|    V    |    **Volatility**. The volatility of the underlying security. This factor usually cannot be directly observed in the market. It is most often calculated by looking at the prices for recent option transactions and back-solving a Black-Scholes style equation to find the volatility that would result in the observed price. This is commonly abbreviated with the Greek letter sigma, σ, although V is used here for consistency with the code below.    |
|    q    |    **Continuous Yield**. Used in the Merton model, this is the continuous yield of the underlying security. Option holders are typically not paid dividends or other payments until they exercise the option. As a result, this factor decreases the value of an option.    |
|    r    |    **Risk Free Rate**. This is expected return on a risk-free investment. This is commonly a approximated by the yield on a low-risk government bond or the rate that large banks borrow between themselves (LIBOR). The rate depends on tenor of the cash flow. For example, a 10-year risk-free bond is likely to have a different rate than a 20-year risk-free bond.    |
|    rf    |    **Foreign Risk Free Rate**. Used in the Garman-Kohlhagen model, this is the risk free rate of the foreign currency. Each currency will have a risk free rate.    |
**Figure 1.** Generalized Black Scholes Formula.

The correction term, b, varies by formula – it differentiates the various Black Scholes formula from one another (see Figure 2). The cost of carry refers to the cost of “carrying” or holding a position. For example, holding a bond may result in earnings from interest, holding a stock may result in stock dividends, or the like. Those payments are made to the owner of the underlying asset and not the owner of the option. As a result, they reduce the value of the option.

|      | Model              | Cost of Carry (b) |
| ---- | ------------------ | ----------------- |
| 1.   | `black_scholes`    | b = r             |
| 2.   | `merton`           | b = r - q         |
| 3.   | `black_76`         | b = 0             |
| 4.   | `garman_kohlhagen` | b = r - rf        |
| 5.   | `asian_76`         | b = 0, modified V |
**Figure 2.** Generalized Black Scholes Cost of Carry Adjustment.


### Asian Volatility Adjustment

An Asian option is an option whose payoff is calculated using the average price of the underlying over some period of time rather than the price on the expiration date. As a result, Asian options are also called average price options. The reason that traders use Asian options is that averaging a settlement price over a period of time reduces the affect of manipulation or unusual price movements on the expiration date on the value of the option. As a result, Asian options are often found on strategically important commodities, like crude oil or in markets with intermittent trading.

The average of a set of random numbers (prices in this case) will have a lower dispersion (a lower volatility) than the dispersion of prices observed on any single day. As a result, the implied volatility used to price Asian options will usually be slightly lower than the implied volatility on a comparable European option. From a mathematical perspective, valuing an Asian option is slightly complicated since the average of a set of log-normal distributions is not itself log-normally distributed. However, a reasonably good approximation of the correct answer is not too difficult to obtain.

In the case of Asian options on futures, it is possible to use a modified Black-76 formula that replaces the implied volatility term with an adjusted implied volatility of the average price.  As long as the first day of the averaging period is in the future, the following formula can be used to value Asian options (see Figure 3).

*Asian Adjusted Volatility*
$$
\begin{equation}
V_a = \sqrt{\frac{ln(M)}{T}}
\end{equation}
$$

with the intermediate calculation

$$
\begin{equation}
M = \frac{2e^{V^2T} - 2e^{V^2T}[1+V^2(T-t)]}{V^4(T-t)^2}
\end{equation}
$$

| Symbol | Meaning |
|--------|-----------------------------------------------------------------------------------------------------------------|
| Va | **Asian Adjusted Volatility**, This will replace the volatility (V) term in the GBS equations shown previously. |
| T | **Time to expiration**. The time to expiration of the option (measured in years).  |
| t_a | **Time to start of averaging period**. The time to the start of the averaging period (measured in years). |

**Figure 3.** Asian Option Formula.


### Spread Option (Kirk's Approximation) Calculation

Spread options are based on the spread between two commodity prices. They are commonly used to model physical investments as "real options" or to mark-to-market contracts that hedge physical assets. For example, a natural gas fueled electrical generation unit can be used to convert fuel (natural gas) into electricity. Whenever this conversion is profitable, it would be rational to operate the unit. This type of conversion is readily modeled by a spread option. When the spread of (electricity prices - fuel costs) is greater than the conversion cost, then the unit would operate. In this example, the conversion cost, which might be called the *Variable Operations and Maintenance* (VOM) for a generation unit, would represent the strike price.

Analytic formulas similar to the Black Scholes equation are commonly used to value commodity spread options. One such formula is called *Kirk’s approximation*. While an exact closed form solution does not exist to value spread options, approximate solutions can give reasonably accurate results.  Kirk’s approximation uses a Black Scholes style framework to analyze the joint distribution that results from the ratio of two log-normal distributions.

In a Black Scholes equation, the distribution of price returns is assumed to be normally distributed on the expiration date. Kirk’s approximation builds on the Black Scholes framework by taking advantage of the fact that the ratio of two log-normal distributions is approximately normally distributed.  By modeling a ratio of two prices rather than the spread between the prices, Kirk’s approximation can use the same formulas designed for options based on a single underlying. In other words, Kirk’s approximation uses an algebraic transformation to fit the spread option into the Black Scholes framework.

The payoff of a spread option is show in Figure 4.

**Figure 4.** Spread Option Payoff.

$$
\begin{equation}
C = max[F_1 - F_2 - X, 0]
\end{equation}
$$

$$
\begin{equation}
P = max[X - (F_1 - F_2), 0]
\end{equation}
$$

Where

| Symbol | Meaning |
|--------|----------------------------------------------------|
| F_1 | **Price of Asset 1**, The prices of the first asset.  |
| F_2 | **Price of Asset 2**. The price of the second asset.  |


**Figure 4.** Spread Option Payoff.

This can be algebraically manipulated as shown in Figure 5.

$$
\begin{equation}
C = max \biggl[\frac{F_1}{F_2+X}-1,0 \biggr](F_2 + X)
\end{equation}
$$

$$
\begin{equation}
P = max \biggl[1-\frac{F_1}{F_2+X},0 \biggr](F_2 + X)
\end{equation}
$$

**Figure 5.** - Spread Option Payoff, Manipulated.

This allows Kirk’s approximation to model the distribution of the spread as the ratio of the price of asset 1 over the price of asset 2 plus the strike price. This ratio can then be converted into a formula very similar to the Generalized Black Scholes formulas. In fact, this is the Black Scholes formula shown above with the addition of a (F_2 + X) term (see Figure 6).

*Ratio of prices*
$$
\begin{equation}
F = \frac{F_1}{F_2 + X}
\end{equation}
$$

The ratio implies that the option is profitable to exercise (*in the money*) whenever the ratio of prices (F in the formula above) is greater than 1. This occurs the cost of the finished product (F_1) exceeds total cost of the raw materials (F_2) and the conversion cost (X). This requires a modification to the Call/Put Price formulas and to the D_1 formula. Because the option is in the money when F>1, the "strike" price used in inner square brackets of the Call/Put Price formulas and the D1 formula is set to 1.

*Spread Option Call Price*

$$
\begin{equation}
C = (F_2 + X)\biggl[Fe^{(b-r)T} N(D_1) - e^{-rT} N(D_2)\biggr]
\end{equation}
$$

*Spread Option Put Price*

$$
\begin{equation}
P = (F_2 + X)\biggl[e^{-rT} N(-D_2) - Fe^{(b-r)T} N(-D_1)\biggr]
\end{equation}
$$

$$
\begin{equation}
D_1 = \frac{ln(F) + (b+\frac{V^2}{2})T}{V*\sqrt{T}}
\end{equation}
$$

$$
\begin{equation}
D_2 = D_1 - V\sqrt{T}
\end{equation}
$$

**Figure 6.** Kirk's Approximation Ratio.

The key complexity is determining the appropriate volatility that needs to be used in the equation. The “approximation” which defines Kirk’s approximation is the assumption that the ratio of two log-normal distributions is normally distributed. That assumption makes it possible to estimate the volatility needed for the modified Black Scholes style equation (see Figure 7).

$$
\begin{equation}
V = \sqrt{ V_1^{2}+ \biggl[V_2\frac{F_2}{F_2+X}\biggr]^2 - 2ρ V_1 V_2 \frac{F_2}{F_2+X} }
\end{equation}
$$

|    Symbol    |    Meaning    |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    V   |    **Volatility**. The Kirk's approximation volatility that will be placed into the formula shown in Figure 6    |
|    V1    |    **Volatility of Asset 1**.   The strike, or exercise, price of the option.    |
|    V2    |    **Volatility of Asset 2**. The volatility of the second asset   |
|    ρ    |    **Correlation**. The correlation between price of asset 1 and the price of asset 2.    |

**Figure 7.** Kirk's Approximation (Volatility).

A second complexity is that the prices of two assets (F1 and F2) have to be in the same units. For example, in a heat rate option, the option represents the ability to convert fuel (natural gas) into electricity. The price of the first asset, electricity, might be quoted in US dollars per megawatt-hour or USD/MWH. However, the price of the second asset might be quoted in USD/MMBTU. To use the approximation, it is necessary to convert the price of the second asset into the units of the first asset (See *Example 1 - a Heat Rate Option*). This conversion rate will typically be specified as part of the contract.

Example: A 10 MMBTU/MWH heat rate call option

* F1 = price of electricity = USD 35/MWH
* F2* = price of natural gas = USD 3.40/MMBTU; *This is not the price to plug into the model!*
* V1 = volatility of electricity forward prices = 35%
* V2 = volatility of natural gas forward price = 35%
* Rho = correlation between electricity and natural gas forward prices = 90%
* VOM = variable operation and maintenance cost (the conversion cost) = USD 3/MWH

Before being placed into a spread option model, the price of natural gas would need to be converted into the correct units.
* F2 = Heat Rate * Fuel Cost = (10 MMBTU/MWH)(USD 3.40/MMBTU) = USD 34/MWH

The strike price would be set equal to the conversion cost
* X = VOM costs = USD 3/MWH

**Example 1.** A Heat Rate Call Option.

Another important consideration (not discussed in this write-up) is that volatility and correlation need to be matched to the tenor of the underlying assets. This means that it is necessary to measure the volatility of forward prices rather than spot prices. It may also be necessary to match the volatility and correlation to the correct month. For example, power prices in August may behave very differently than power prices in October or May in certain regions.

Like any model, spread options are subject to the "garbage in = garbage out" problem. However, the relative complexity of modeling commodity prices (the typical underlying for spread options) makes calibrating inputs a key part of the model.


### American Options
American options differ from European options because they can be exercised at any time. If there is a possibility that it will be more profitable to exercise the option than sell it, an American option will have more value than a corresponding European option. Early exercise typically occurs only when an option is *in the money*. If an option is out of the money, there is usually no reason to exercise early - it would be better to sell the option (in the case of a put option, to sell the option and the underlying asset).

The decision of whether to exercise early is primarily a question of interest rates and carrying costs. Carrying costs, or *cost of carry*, is a term that means an intermediate cash flows that is the result of holding an asset. For example, dividends on stocks are a positive cost of carry (owning the asset gives the owner a cash flow). A commodity might have a negative cost of carry. For example, a commodity that requires its owner to pay for storage would cause the owner of the physical commodity to pay cash to hold the asset. (**Note:** Commodity options are typically written on forwards or futures which have zero cost of carry instead of the actual underlying commodity). Cost of carry is cash flow that affects the owner of the underlying commodity and not the owner of the option. For example, when a stock pays a dividend, the owner of a call option does not receive the dividend - just the owner of the stock. For the perspective for the owner of a call option on a stock, the cost of carry will be the interest received from holding cash (r) less any dividends paid to owners of the stock (q).

Since an option has some value (the *extrinsic value*) that would be given up by exercising the option, exercising an option prior to maturity is a trade off between the option's extrinsic value (the remaining optionality) and the relative benefit of holding cash (time value of money) versus the benefit of holding the asset (carrying costs).

The early exercise feature of **American equity put options** may have value when:
* The cost of carry on the asset is low - preferably zero or negative.
* Interest rates are high
* The option is in the money

The early exercise feature of **American equity call options** may have value when:
* The cost of carry on the asset is positive
* Interest rates are low or negative
* The option is in the money

With commodities, things are a slightly different. There is typically no cost of carry since the underlying is a forward or a futures contract. It does not cost any money to enter an at-the-money commodity forward, swap, or futures contract. Also, these contracts don't have any intermediate cash flows. As a result, the primary benefit of early exercise is to get cash immediately (exercising an in-the-money option) rather than cash in the future. In high interest rate environments, the money received immediately from immediate execution may exceed the extrinsic value of the contract. This is due to strike price not being present valued in immediate execution (it is specified in the contract and a fixed number) but the payoff of a European option is discounted (forward price - strike price).

The overall result is that early exercise is fairly uncommon for most commodity options. Typically, it only occurs when interest rates are high. Generally, interest rates have to be higher than 15%-20% for American commodity options to differ substantially in value from European options with the same terms.

The early exercise feature of **American commodity options** has value when:
* Interest rates are high
* Volatility is low (this makes selling the option less of a good option)
* The option is in the money

There is no exact closed-form solution for American options. However, there are many approximations that are reasonably close to prices produced by open-form solutions (like binomial tree models). Two models are shown below, both created by Bjerksund and Stensland. The first was produced in 1993 and the second in 2002. The second model is a refinement of the first model, adding more complexity, in exchange for better accuracy.

#### Put-Call Parity
Because of Put/Call parity, it is possible to use a call valuation formula to calculate the value of a put option.

$$
\begin{equation}
P(S,X,T,r,b,V) = C(X,S,T,r-b,-b,V)
\end{equation}
$$

or using the order of parameters used in this library:

$$
\begin{equation}
P(X,S,T,b,r,V) = C(S,X,T,-b,r-b,V)
\end{equation}
$$

#### Bjerksund Stensland 1993 (BS1993)
There is no closed form solution for American options, and there are multiple people who have developed closed-form approximations to value American options. This is one such approximation. However, this approximation is no longer in active use by the public interface. It is primarily included as a secondary test on the BS2002 calculation. This function uses a numerical approximation to estimate the value of an American option. It does this by estimating a early exercise boundary and analytically estimating the probability of hitting that boundary. This uses the same inputs as a Generalized Black Scholes model:

```
    FS = Forward or spot price (abbreviated FS in code, F in formulas below)
    X = Strike Price
    T = time to expiration
    r = risk free rate
    b = cost of carry
    V = volatility
```

_Intermediate Calculations_. To be consistent with the Bjerksund Stensland paper, this write-up uses similar notation. Please note that both a capital B (B_0 and B_Infinity), a lower case b, and the Greek symbol Beta are all being used. B_0 and B_infinity represent that optimal exercise boundaries in edge cases (for call options where T=0 and T=infinity respectively), lower case b is the cost of carry (passed in as an input), and Beta is an intermediate calculations.

$$
\begin{array}{lcl}
\beta & = & (0.5 - \frac{b}{V^2}) + \sqrt{(\frac{b}{V^2} - 0.5)^2 + 2 \frac{r}{V^2}} \\
B_\infty & = & \frac{\beta}{\beta-1} X \\
B_0 & = & max\biggl[X, (\frac{r}{r-b}) X\biggr] \\
h_1 & = & - b T + 2 V \sqrt{T} \frac{B_0}{B_\infty-B_0} \\
\end{array}
$$

_Calculate the Early Exercise Boundary (i)_. The lower case i represents the early exercise boundary. Alpha is an intermediate calculation.

$$
\begin{array}{lcl}
i & = & B_0 + (B_\infty-B_0)(1 - e^{h_1} ) \\
\alpha & = & (i-X) i^{-\beta}
\end{array}
$$

Check for immediate exercise.

$$
\begin{equation}
if F >= i, then Value = F - X
\end{equation}
$$

If no immediate exercise, approximate the early exercise price.

$$
\begin{eqnarray}
Value & = & \alpha * F^\beta \\
& - & \alpha * \phi(F,T,\beta,i,i,r,b,V) \\
& + & \phi(F,T,1,i,i,r,b,V) \\
& - & \phi(F,T,1,X,i,r,b,V) \\
& - & X * \phi(F,T,0,i,i,r,b,V) \\
& + & X * \phi(F,T,0,X,i,r,b,V)
\end{eqnarray}
$$

_Compare to European Value_.
Due to the approximation, it is sometime possible to get a value slightly smaller than the European value. If so, set the value equal to the European value estimated using Generalized Black Scholes.
$$
\begin{equation}
Value_{BS1993} = Max \biggl[ Value, Value_{GBS} \biggr]
\end{equation}
$$

#### Bjerksund Stensland 2002 (BS2002)
Source: https://www.researchgate.net/publication/228801918

```
    FS = Forward or spot price (abbreviated FS in code, F in formulas below)
    X = Strike Price
    T = time to expiration
    r = risk free rate
    b = cost of carry
    V = volatility
```

#### Psi
Psi is an intermediate calculation used by the Bjerksund Stensland 2002 approximation.

$$
\begin{equation}
\psi(F, t_2, \gamma, H, I_2, I_1, t_1, r, b, V)
\end{equation}
$$

_Intermediate calculations_.
The Psi function has a large number of intermediate calculations. For clarity, these are loosely organized into groups with each group used to simplify the next set of intermediate calculations.

$$
\begin{array}{lcl}
A_1 & = & V \ln(t_1) \\
A_2 & = & V \ln(t_2) \\
B_1 & = & \biggl[ b+(\gamma-0.5) V^2 \biggr] t_1 \\
B_2 & = & \biggl[ b+(\gamma-0.5) V^2 \biggr] t_2
\end{array}
$$

More Intermediate calculations

$$
\begin{array}{lcl}
d_1 & = & \frac{ln(\frac{F}{I_1}) + B_1}{A_1} \\
d_2 & = & \frac{ln(\frac{I_2^2}{F I_1}) + B_1}{A_1} \\
d_3 & = & \frac{ln(\frac{F}{I_1}) - B_1}{A_1} \\
d_4 & = & \frac{ln(\frac{I_2^2}{F I_1}) - B_1}{A_1} \\
e_1 & = & \frac{ln(\frac{F}{H}) + B_2}{A_2} \\
e_2 & = & \frac{ln(\frac{I_2^2}{F H}) + B_2}{A_2} \\
e_3 & = & \frac{ln(\frac{I_1^2}{F H}) + B_2}{A_2} \\
e_4 & = & \frac{ln(\frac{F I_1^2}{H I_2^2}) + B_2}{A_2}
\end{array}
$$

Even More Intermediate calculations

$$
\begin{array}{lcl}
\tau & = & \sqrt{\frac{t_1}{t_2}} \\
\lambda & = & -r+\gamma b+\frac{\gamma}{2} (\gamma-1) V^2 \\
\kappa & = & \frac{2b}{V^2} +(2 \gamma - 1)
\end{array}
$$

_The calculation of Psi_.
This is the actual calculation of the Psi function. In the function below, M() represents the cumulative bivariate normal distribution (described a couple of paragraphs below this section). The abbreviation M() is used instead of CBND() in this section to make the equation a bit more readable and to match the naming convention used in Haug's book "The Complete Guide to Option Pricing Formulas".

$$
\begin{eqnarray}
\psi & = & e^{\lambda t_2} F^\gamma M(-d_1, -e_1, \tau) \\
& - & \frac{I_2}{F}^\kappa M(-d_2, -e_2, \tau) \\
& - & \frac{I_1}{F}^\kappa M(-d_3, -e_3, -\tau) \\
& + & \frac{I_1}{I_2}^\kappa M(-d_4, -e_4, -\tau))
\end{eqnarray}
$$

#### Phi
Phi is an intermediate calculation used by both the Bjerksun Stensland 1993 and 2002 approximations. Many of the parameters are the same as the GBS model.

$$
\begin{equation}
\phi(FS, T, \gamma, h, I, r, b, V)
\end{equation}
$$

```
    FS = Forward or spot price (abbreviated FS in code, F in formulas below).
    T = time to expiration.
    I =  trigger price (as calculated in either BS1993 or BS2002 formulas
    gamma = modifier to T, calculated in BS1993 or BS2002 formula
    r = risk free rate.
    b = cost of carry.
    V = volatility.
```

Internally, the `Phi()` function is implemented as follows:

$$
\begin{equation}
d_1 = -\frac{ln(\frac{F}{h}) + \biggl[b+(\gamma-0.5) V^2 \biggr] T}{V \sqrt{T}}
\end{equation}
$$

$$
\begin{equation}
d_2 = d_1 - 2 \frac{ln(I/F)}{V \sqrt(T)}
\end{equation}
$$

$$
\begin{equation}
\lambda = -r+\gamma b+0.5 \gamma (\gamma-1) V^2
\end{equation}
$$

$$
\begin{equation}
\kappa = \frac{2b}{V^2}+(2\gamma-1)
\end{equation}
$$

$$
\begin{equation}
\phi = e^{\lambda T} F^{\gamma} \biggl[ N(d_1)-\frac{I}{F}^{\kappa} N(d_2) \biggr]
\end{equation}
$$

##### Normal Cumulative Density Function (N)
This is the normal cumulative density function. It can be found described in a variety of statistical textbooks and/or Wikipedia. It is part of the standard `scipy.stats` distribution and imported using the `from scipy.stats import norm` command.

Example:

$$
\begin{equation}
    N(d_1)
\end{equation}
$$

#### Cumulative bivariate normal distribution (CBND)
The bivariate normal density function (BNDF) is given below (see Figure 8):

$$
\begin{equation}
BNDF(x, y) =  \frac{1}{2 \pi \sqrt{1-p^2}} exp \biggl[-\frac{x^2-2pxy+y^2}{2(1-p^2)}\biggr]
\end{equation}
$$

**Figure 8.** Bivariate Normal Density Function (BNDF).

This can be integrated over x and y to calculate the joint probability that x < a and y < b. This is called the cumulative bivariate normal distribution (CBND; see Figure 9):

$$
\begin{equation}
CBND(a, b, p) = \frac{1}{2 \pi \sqrt{1-p^2}} \int_{-\infty}^{a} \int_{-\infty}^{b} exp \biggl[-\frac{x^2-2pxy+y^2}{2(1-p^2)}\biggr] d_x d_y
\end{equation}
$$

**Figure 9.** Cumulative Bivariate Normal Distribution (CBND).

Where
* x = the first variable
* y = the second variable
* a = upper bound for first variable
* b = upper bound for second variable
* p = correlation between first and second variables

There is no closed-form solution for this equation. However, several approximations have been developed and are included in the `numpy` library distributed with Anaconda. The Genz 2004 model was chosen for implementation. Alternative models include those developed by Drezner and Wesolowsky (1990) and Drezner (1978). The Genz model improves these other model by going to an accuracy of 14 decimal points (from approximately 8 decimal points and 6 decimal points respectively).

## Limitations
These functions have been tested for accuracy within an allowable range of inputs (see "Model Input" section below). However, general modeling advice applies to the use of the model. These models depend on a number of assumptions. In plain English, these models assume that the distribution of future prices can be described by variables like implied volatility. To get good results from the model, the model should only be used with reliable inputs.

The following limitations are also in effect:

1. The Asian Option approximation shouldn't be used for Asian options that are into the Asian option calculation period.
2. The American and American76 approximations break down when `r` < -20%. The limits are set wider in this example for testing purposes, but production code should probably limit interest rates to values between -20% and 100%. In practice, negative interest rates should be extremely rare.
3. No Greeks are produced for spread options
4. These models assume a constant volatility term structure. This has no effect on European options. However, options that are likely to be exercise early (certain American options) and Asian options may be more affected.

## Model Inputs
This section describes the function calls an inputs needed to call this model:

These functions encapsulate the most commonly encountered option pricing formulas. These function primarily figure out the cost-of-carry term (b) and then call the generic version of the function. All of these functions return an array containing the premium and the Greeks.

#### Public Functions in the Library

Pricing Formulas:
       1. `black_scholes(option_type, fs, x, t, r, v)`
    2. `merton(option_type, fs, x, t, r, q, v)`
    3. `black_76(option_type, fs, x, t, r, v)`
    4. `garman_kohlhagen(option_type, fs, x, t, b, r, rf, v)`
    5. `asian_76(option_type, fs, x, t, t_a, r, v)`
    6. `kirks_76(option_type, f1, f2, x, t, r, v1, v2, corr)`
    7. `american(option_type, fs, x, t, r, q, v)`
    8. `american_76(option_type, fs, x, t, r, v)`

Implied Volatility Formulas
       9. `euro_implied_vol(option_type, fs, x, t, r, q, cp)`
    10. `euro_implied_vol_76(option_type, fs, x, t, r, cp)`
    11. `amer_implied_vol(option_type, fs, x, t, r, q, cp)`
    12. `amer_implied_vol_76(option_type, fs, x, t, r, cp)`

#### Inputs used by all models
| **Parameter** | **Description**                                              |
| ------------- | ------------------------------------------------------------ |
| `option_type` | **Put/Call Indicator** Single character, `"c"` indicates a call; `"p"` a put |
| `fs`          | **Price of Underlying** `fs` is generically used, but for specific models, the following abbreviations may be used: F = Forward Price, S = Spot Price) |
| `x`           | **Strike Price**                                             |
| `t`           | **Time to Maturity** This is in years (1.0 = 1 year, 0.5 = six months, etc) |
| `r`           | **Risk Free Interest Rate** Interest rates (0.10 = 10% interest rate) |
| `v`           | **Implied Volatility** Annualized implied volatility (1 = 100% annual volatility, 0.34 = 34% annual volatility) |

#### Inputs used by some models
| **Parameter** | **Description**                                                                                                                                      |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| `b`           | **Cost of Carry** This is only found in internal implementations, but is identical to the cost of carry (`b`) term commonly found in academic option pricing literature |
| `q`           | **Continuous Dividend** Used in Merton and American models; Internally, this is converted into cost of carry, `b`, with formula `b = r - q`          |
| `rf`          | **Foreign Interest Rate** Only used GK model; this functions similarly to `q`                                                                        |
| `t_a`           | **Asian Start** Used for Asian options; This is the time that starts the averaging period (`t_a`=0 means that averaging starts immediately). As `t_a` approaches `t`, the Asian value should become very close to the Black76 Value |
| `cp`           | **Option Price** Used in the implied vol calculations; This is the price of the call or put observed in the market |


#### Outputs
All of the option pricing functions return an array. The first element of the array is the value of the option, the other elements are the Greeks which measure the sensitivity of the option to changes in inputs. The Greeks are used primarily for risk-management purposes.

| **Output** | **Description**                                                                                                   |
|------------|-------------------------------------------------------------------------------------------------------------------|
| [0]        | **Value**                                                                                                         |
| [1]        | **Delta**  Sensitivity of Value to changes in price                                                               |
| [2]        | **Gamma** Sensitivity of Delta to changes in price                                                                |
| [3]        | **Theta** Sensitivity of Value to changes in time to expiration (annualized). To get a daily Theta, divide by 365 |
| [4]        | **Vega** Sensitivity of Value to changes in Volatility                                                            |
| [5]        | **Rho** Sensitivity of Value to changes in risk-free rates.                                                       |

The implied volatility functions return a single value (the implied volatility).

#### Acceptable Range for inputs
All of the inputs are bounded. While many of these functions will work with inputs outside of these bounds, they haven't been tested and are generally believed to be uncommon. The pricer will return an exception to the caller if an out-of-bounds input is used. If that was a valid input, the code below will need to be modified to allow wider inputs and the testing section updated to test that the models work under the widened inputs.
