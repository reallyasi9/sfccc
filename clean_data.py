#!/usr/bin/python3

"""
Clean the data and create processed train, test, and key files.

Run this over the data first.  Make sure you downloaded the data from the
appropriate places.
"""
import sys

__author__ = 'pkillewald'

import pandas


def main():
    truth_df = pandas.DataFrame.from_csv("raw_data/truth.csv", index_col=None)
    # Generate "Dates" from "Date" and "Time"
    truth_df["Dates"] = pandas.to_datetime(truth_df["Date"] + " " + truth_df["Time"])
    # Remove commas from Category field, because they are removed from the train and submission sets
    truth_df["Category"] = truth_df["Category"].apply(lambda x: x.replace(",", ""))

    train_df = pandas.DataFrame.from_csv("raw_data/train.csv", index_col=None)
    train_df["Dates"] = pandas.to_datetime(train_df["Dates"])

    test_df = pandas.DataFrame.from_csv("raw_data/test.csv", index_col=None)
    test_df["Dates"] = pandas.to_datetime(test_df["Dates"])

    # Those entries at the North Pole are missing data.
    # They do appear in the test set, which kills me.
    # Here are what their addresses look like
    invalid_train_points = (train_df["Y"] == 90)
    invalid_truth_points = (truth_df["Y"] == 90)
    invalid_test_points = (test_df["Y"] == 90)

    # It turns out that most of these problems are because the city's grid system
    # is busted up by Market St, and the streets on the west side of Market have
    # a different name from the connecting streets on the east side.
    #
    # And some times, it's a similar problem, only on the grid system, where one
    # road suddenly changes names.
    #
    # And some times, the streets are input wrong, so they never intersect.
    #
    # These solutions come from looking up the intersections in Google manually.
    # Sometimes I had to guess as to what the real streats were that they were talking about.
    bad_addresses = ["7THSTNORTH ST / MCALLISTER ST",
                     "GEARY BL / AVENUE OF THE PALMS",

                     'EDDY ST / 5THSTNORTH ST',
                     'MCALLISTER ST / 7THSTNORTH ST',

                     'FRONT ST / THE EMBARCADERONORTH ST',
                     'OFARRELL ST / 5THSTNORTH ST',

                     '5TH ST / 5THSTNORTH ST',
                     'STJOSEPHS AV / TERRAVISTA AV',

                     'AUSTIN ST / LARKIN ST',
                     'ELLIS ST / 5THSTNORTH ST',

                     '5THSTNORTH ST / EDDY ST',
                     'JENNINGS CT / PHELPS ST',

                     'INTERSTATE280 HY / GENEVA AV',
                     'ELLICK LN / CALIFORNIA ST',

                     'BUSH ST / STGEORGE AL',
                     'INTERSTATE280 HY / OCEAN AV',

                     'SPEAR ST / THE EMBARCADEROSOUTH ST',
                     'BRANNAN ST / 1ST ST',

                     'ARGUELLO BL / NORTHRIDGE DR',
                     '17TH ST / COLLINGWOOD ST',

                     'JEWETT ST / 5TH ST',
                     'JAMES LICK FREEWAY HY / CESAR CHAVEZ ST',

                     'I-280 / CESAR CHAVEZ ST',
                     'JAMES LICK FREEWAY HY / 4TH ST',

                     'JAMES LICK FREEWAY HY / SILVER AV',
                     '1ST ST / BRYANT ST',

                     'LARKIN ST / AUSTIN ST',
                     'JOHN F KENNEDY DR / CROSSOVER DR',

                     'EUCLID AV / AVENUE OF THE PALMS',
                     'GILMAN AV / FITCH ST',

                     '1ST ST / BRANNAN ST',
                     'JAMES LICK FREEWAY HY / BAY SHORE BL',

                     'SPEAR ST / THE EMBARCADERO SOUTH ST',
                     'LOWER GREAT HY / MARTIN LUTHER KING JR DR',

                     '5THSTNORTH ST / OFARRELL ST',
                     'JAMESLICKFREEWAY HY / SILVER AV',

                     '5THSTNORTH ST / ELLIS ST',
                     'YOSEMITE AV / WILLIAMS AV',

                     'BRENHAM PL / WASHINGTON ST',
                     'AVENUE OF THE PALMS / GEARY BL',

                     'STCHARLES AV / 19TH AV',
                     'TURK ST / STJOSEPHS AV',

                     'MONTGOMERY ST / THE EMBARCADERONORTH ST',
                     'FITCH ST / DONNER AV',

                     'AVENUE OF THE PALMS / EUCLID AV',
                     'VANNESS AV / BEACH ST',

                     'PERSIA AV / LAGRANDE AV',
                     '3RD ST / ISLAISCREEK ST',

                     'JENNINGS CT / INGALLS ST',
                     'GENEVA AV / INTERSTATE280 HY',

                     'CHARLES J BRENHAM PL / CLAY ST',
                     'STELMO WY / MONTEREY BL',

                     'I-280 / PENNSYLVANIA AV',
                     'FLORIDA ST / ALAMEDA ST',

                     'BRYANT ST / SPEAR ST',
                     'PERSIA AV / LA GRANDE AV',

                     'GREENWICH ST / THE EMBARCADERO NORTH ST',
                     'JOHN F KENNEDY DR / MARTIN LUTHER KING JR DR',

                     '3RD ST / JAMES LICK FREEWAY HY'
                     ]

    solution_latlon = [(37.781002, -122.413187),  # 7th -> Charles J. Brenham Pl
                       (37.781391, -122.457743),
                       # Avenue of the Palms -> Palm Ave (Avenue of the Palms is on Treasure Island)

                       (37.784466, -122.408574),  # 5th -> Cyril Magnin St
                       (37.781002, -122.413187),  # 7th -> Charles J. Brenham Pl

                       (37.801544, -122.400441),  # The Embarcadero -> Union St (Front St ends before intersecting TE)
                       (37.786336, -122.408949),  # 5th -> Cyril Magnin St

                       (37.784010, -122.408097),  # Best guess: Market St?
                       (37.781236, -122.441349),  # Terra Vista Ave -> Ellis St

                       (37.789378, -122.418782),  # Austin St -> Frank Norris St
                       (37.785413, -122.408753),  # 5th -> Cyril Magnin St

                       (37.784466, -122.408574),  # 5th -> Cyril Magnin St
                       (37.717177, -122.397460),
                       # Jennings Ct is nowhere near Phelps Ave, and Jennings St is parallel to Phelps?

                       (37.721288, -122.448127),  # No changes
                       (37.793165, -122.400530),
                       # Ellick Ln doesn't exist?  This is in the middle of California St by Halleck St

                       (37.790727, -122.404352),  # No changes
                       (37.722981, -122.447773),  # No changes

                       (37.787690, -122.387976),  # Spear St is a pedestrian walkway at the intersection
                       (37.783652, -122.389865),  # 1st -> Delancey St

                       (37.773227, -122.459070),  # No idea.  Northridge Dr doesn't exist.  I put this in the park?
                       (37.762138, -122.436218),  # 17th -> Market St (Collingwood ends at Market)

                       (37.784005, -122.408090),  # No idea.  Jewett is not actually a street.  I put this at Market?
                       (37.749387, -122.403732),  # No changes

                       (37.750103, -122.391998),  # No changes
                       (37.780262, -122.398896),  # No changes

                       (37.732664, -122.405247),  # No changes
                       (37.784950, -122.391289),  # Approximate (1st ends before intersecting Bryant)

                       (37.789378, -122.418782),  # Austin St -> Frank Norris St
                       (37.770716, -122.479205),  # No changes

                       (37.783870, -122.457922),
                       # Avenue of the Palms -> Palm Ave (Avenue of the Palms is on Treasure Island)
                       (37.717177, -122.386260),  # No changes

                       (37.783652, -122.389865),  # 1st -> Delancey St
                       (37.715933, -122.398576),  # No changes

                       (37.787690, -122.387976),  # Spear St is a pedestrian walkway at the intersection
                       (37.764097, -122.509411),  # Great Hwy -> La Playa St

                       (37.786336, -122.408949),  # 5th -> Cyril Magnin St
                       (37.732664, -122.405247),  # No changes

                       (37.785413, -122.408753),  # 5th -> Cyril Magnin St
                       (37.729587, -122.394912),  # Yosemite -> Mendell

                       (37.793917, -122.416326),
                       # No idea (Brenham does not intersect Washington.  Brenham -> Leavenworth?)
                       (37.781391, -122.457743),
                       # Avenue of the Palms -> Palm Ave (Avenue of the Palms is on Treasure Island)

                       (37.713785, -122.469331),  # St. Chalres becomes 19th
                       (37.779396, -122.440936),  # No changes

                       (37.806569, -122.405870),  # Montgomery becomes a pedestrian walkway at the intersection
                       (37.719108, -122.384525),  # Approximate (Donner ends before Fitch)

                       (37.783870, -122.457922),
                       # Avenue of the Palms -> Palm Ave (Avenue of the Palms is on Treasure Island)
                       (37.806036, -122.425514),  # Beech ends before Van Ness

                       (37.718562, -122.426440),  # LaGrande -> Dublin St
                       (37.747707, -122.387248),  # Best guess for Islias Creek St?

                       (37.734113, -122.379523),  # Jennings -> Middlepoint Rd (unclear)?
                       (37.721288, -122.448127),  # No changes

                       (37.793043, -122.416116),  # Brenham -> Leavenworth?
                       (37.730460, -122.460551),  # No changes

                       (37.757690, -122.392347),  # No changes
                       (37.768121, -122.411724),  # Approximate (Alameda ends before Florida)

                       (37.787690, -122.387976),  # Spear St is a pedestrian walkway at the intersection
                       (37.718562, -122.426440),  # LaGrande -> Dublin St

                       (37.803124, -122.401270),  # In a shopping mall
                       (37.766686, -122.506270),  # Martin Luther King Jr -> Bernice Rodgers Way

                       (37.781978, -122.396687)  # Very tricky
                       ]

    for address, latlon in zip(bad_addresses, solution_latlon):
        train_df.loc[invalid_train_points & (train_df["Address"] == address), ["Y", "X"]] = latlon
        truth_df.loc[invalid_truth_points & (truth_df["Address"] == address), ["Y", "X"]] = latlon
        test_df.loc[invalid_test_points & (test_df["Address"] == address), ["Y", "X"]] = latlon

    # Before matching, round X and Y to 6 decimal places to avoid FP errors.
    # Note: 6 decimal places lon and lat at this latitude corresponds to ~ 14 cm
    for df in [train_df, truth_df, test_df]:
        df[["X", "Y"]] = df[["X", "Y"]].apply(lambda x: x.round(6), axis="index")

    # There might be differences in address and how the crime was resolved, but not in X or Y anymore
    merged_train_df = train_df.merge(truth_df,
                                     on=[col for col in train_df.columns.tolist() if
                                         col not in ["Address", "Resolution"]],
                                     how="left")

    if merged_train_df["PdId"].isnull().any():
        print("WARNING:  The following training data cannot be merged to the truth data:")
        print(merged_train_df.loc[merged_train_df["PdId"].isnull(), train_df.columns])

    # Match with the test set to label them with the truth
    merged_test_df = test_df.merge(truth_df,
                                   on=[col for col in test_df.columns.tolist() if col not in ["Address", "Id"]],
                                   how="left",
                                   )

    if merged_test_df["PdId"].isnull().any():
        print("WARNING:  The following test data cannot be merged to the truth data:")
        print(merged_test_df.loc[merged_test_df["PdId"].isnull(), test_df.columns])

    # Anyway, save cleaned data to use for future training and testing
    train_df.to_csv("processed_data/train_clean.csv", index=None)
    test_df.to_csv("processed_data/test_clean.csv", index="Id")
    truth_df.to_csv("processed_data/truth_clean.csv", index=None, columns=train_df.columns)

    # Finally, produce an (almost) correct key for the test set
    # Note: the ones I can't figure out I am leaving completely blank.
    key = pandas.get_dummies(merged_test_df[["Id", "Category"]], columns=["Category"], prefix=[""], prefix_sep="")
    key = key.groupby("Id").mean()
    key.to_csv("processed_data/key.csv", index="Id")

    return

if __name__ == "__main__":
    main()
    sys.exit(0)
