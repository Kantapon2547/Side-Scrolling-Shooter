import pandas as pd
import matplotlib.pyplot as plt


class StatisticsManager:
    """Handles recording and reporting game statistics."""

    def __init__(self):
        try:
            self.df = pd.read_csv('data_collection.csv')  # Load CSV on initialization
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.df = pd.DataFrame()  # Prevent crash

    def analyze_damage(self):
        """Generate a histogram of damage taken during the game."""
        if 'Health Lost' not in self.df.columns:
            print("Column 'Health Lost' not found in CSV.")
            return

        plt.figure(figsize=(8, 6))
        plt.hist(self.df['Health Lost'], bins=10, edgecolor='black', color='skyblue')
        plt.xlabel('Health Lost')
        plt.ylabel('Frequency')
        plt.title('Histogram of Damage Taken')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def analyze_bullets_fired(self):
        """Generate a scatter plot of bullets fired during the game."""
        if 'Bullets Fired' not in self.df.columns:
            print("Column 'Bullets Fired' not found in CSV.")
            return

        plt.figure(figsize=(8, 6))
        plt.scatter(self.df.index, self.df['Bullets Fired'], color='orange', label='Bullets Fired')
        plt.xlabel('Game Instance')
        plt.ylabel('Number of Bullets Fired')
        plt.title('Scatter Plot of Bullets Fired')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def analyze_health_remaining(self):
        """Generate a box plot of health remaining, grouped by level, to analyze difficulty consistency."""
        if 'Health Remaining' not in self.df.columns:
            print("Column 'Health Remaining' not found in CSV.")
            return
        if 'Level' not in self.df.columns:
            print("Column 'Level' not found in CSV.")
            return

        plt.figure(figsize=(10, 6))
        self.df.boxplot(column='Health Remaining', by='Level', grid=True)
        plt.title('Health Remaining by Level')
        plt.suptitle('')  # Remove the automatic 'Boxplot grouped by Level' subtitle
        plt.xlabel('Level')
        plt.ylabel('Health Remaining')
        plt.tight_layout()
        plt.show()

    def analyze_grenade_usage_lineplot(self):
        """Generate a line plot of grenade usage, showing trends across levels."""
        if 'Grenades Thrown' not in self.df.columns:
            print("Column 'Grenades Thrown' not found in CSV.")
            return
        if 'Level' not in self.df.columns:
            print("Column 'Level' not found in CSV.")
            return

        # Clean data as above
        self.df['Grenades Thrown'] = pd.to_numeric(self.df['Grenades Thrown'], errors='coerce')
        self.df.dropna(subset=['Grenades Thrown'], inplace=True)

        # Group by 'Level' and calculate the mean grenade usage for each level
        grenade_usage_by_level = self.df.groupby('Level')['Grenades Thrown'].mean()

        # Plot the line plot
        plt.figure(figsize=(10, 6))
        grenade_usage_by_level.plot(kind='line', marker='o', color='green', linestyle='-', linewidth=2, markersize=8)
        plt.title('Average Grenades Thrown by Level')
        plt.xlabel('Level')
        plt.ylabel('Average Grenades Thrown')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def record_deaths_per_level(self):
        """Record the number of deaths per level per playthrough."""
        if 'Deaths' not in self.df.columns or 'Level' not in self.df.columns:
            print("Required columns 'Deaths' or 'Level' not found in CSV.")
            return

        # Create a new column that stores the deaths per playthrough
        self.df['Deaths Per Playthrough'] = self.df.groupby('Level')['Deaths'].transform('sum')
        print("Deaths per Level Per Playthrough recorded successfully.")

    def analyze_max_deaths(self):
        """Find the hardest level by identifying the level with maximum deaths."""
        if 'Deaths' not in self.df.columns or 'Level' not in self.df.columns:
            print("Required columns 'Deaths' or 'Level' not found in CSV.")
            return

        # Group by 'Level' and calculate the max deaths per level
        max_deaths = self.df.groupby('Level')['Deaths'].max().reset_index()
        hardest_level = max_deaths[max_deaths['Deaths'] == max_deaths['Deaths'].max()]

        print("Level with Maximum Deaths (Hardest Level):")
        print(hardest_level)
        return hardest_level

    def analyze_death_variation(self):
        """Analyze the variation in deaths per level using standard deviation."""
        if 'Deaths' not in self.df.columns or 'Level' not in self.df.columns:
            print("Required columns 'Deaths' or 'Level' not found in CSV.")
            return

        # Group by 'Level' and calculate the standard deviation of deaths
        death_variation = self.df.groupby('Level')['Deaths'].std().reset_index()
        death_variation = death_variation.rename(columns={'Deaths': 'Death Std Dev'})

        print("Standard Deviation of Deaths Per Level:")
        print(death_variation)
        return death_variation

    def analyze_death_difficulty(self):
        """Analyze difficulty based on maximum deaths and standard deviation."""
        max_deaths = self.analyze_max_deaths()
        death_variation = self.analyze_death_variation()

        # Merge both dataframes on 'Level'
        difficulty_analysis = pd.merge(max_deaths, death_variation, on='Level')

        # Analyze for difficult/inconsistent levels
        difficulty_analysis['Difficulty Score'] = difficulty_analysis['Deaths'] + difficulty_analysis['Death Std Dev']

        print("\nDifficulty Analysis (Maximum Deaths + Standard Deviation):")
        print(difficulty_analysis)
        return difficulty_analysis

    def show_all_stats(self, back_callback=None):
        """Displays all available statistics graphs."""
        import matplotlib
        matplotlib.use("TkAgg")
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        import tkinter as tk
        from tkinter import ttk
        import numpy as np

        if self.df.empty:
            print("No statistics data found to display.")
            return

        def update_plot(choice):
            fig.clf()  # Clear the figure to prepare for a new plot
            ax = fig.add_subplot(111)

            if choice == 'Histogram of Damage Taken':
                if 'Health Lost' in self.df.columns:
                    ax.hist(self.df['Health Lost'].dropna(), bins=10, edgecolor='black', color='skyblue')
                    ax.set_title('Histogram of Damage Taken')
                    ax.set_xlabel('Health Lost')
                    ax.set_ylabel('Frequency')
                else:
                    ax.text(0.5, 0.5, "Column 'Health Lost' not found", ha='center', va='center')

            elif choice == 'Bullets Fired Over Games':
                if 'Bullets Fired' in self.df.columns:
                    ax.scatter(self.df.index, self.df['Bullets Fired'], color='orange')
                    ax.set_title('Scatter Plot of Bullets Fired')
                    ax.set_xlabel('Game Instance')
                    ax.set_ylabel('Bullets Fired')
                else:
                    ax.text(0.5, 0.5, "Column 'Bullets Fired' not found", ha='center', va='center')

            elif choice == 'Health Remaining by Level':
                if 'Current Health' in self.df.columns and 'Level' in self.df.columns:
                    self.df.boxplot(column='Current Health', by='Level', ax=ax, grid=True)
                    ax.set_title('Health Remaining by Level')
                    fig.suptitle('')
                    ax.set_xlabel('Level')
                    ax.set_ylabel('Health Remaining')
                else:
                    ax.text(0.5, 0.5, "Required columns not found", ha='center', va='center')

            elif choice == 'Grenade Usage Lineplot':
                if 'Grenades Thrown' in self.df.columns and 'Level' in self.df.columns:
                    grouped = self.df.groupby('Level')['Grenades Thrown'].mean()
                    grouped.plot(kind='line', marker='o', ax=ax, grid=True)
                    ax.set_title('Average Grenades Thrown by Level')
                    fig.suptitle('')
                    ax.set_xlabel('Level')
                    ax.set_ylabel('Average Grenades Thrown')
                else:
                    ax.text(0.5, 0.5, "Required columns not found", ha='center', va='center')

            elif choice == 'Deaths Per Level Analysis':
                # Analyze deaths and show the results in a text box
                hardest_level = self.analyze_max_deaths()
                death_variation = self.analyze_death_variation()
                difficulty_report = self.analyze_death_difficulty()

                # Create a Text widget to display the death analysis
                result_text.delete(1.0, tk.END)  # Clear any previous text
                result_text.insert(tk.END, "Hardest Level (Maximum Deaths):\n")
                result_text.insert(tk.END, hardest_level.to_string(index=False))
                result_text.insert(tk.END, "\n\nDeath Variation (Standard Deviation):\n")
                result_text.insert(tk.END, death_variation.to_string(index=False))
                result_text.insert(tk.END, "\n\nDifficulty Report (Max Deaths + Std Dev):\n")
                result_text.insert(tk.END, difficulty_report.to_string(index=False))

            canvas.draw()

        # Setup GUI
        win = tk.Tk()
        win.title("Game Statistics Viewer")
        win.configure(bg='black')

        tk.Label(win, text="Select a statistic to view:", bg='black', fg='white', font=("Arial", 14, "bold")).pack(
            pady=10)

        combo = ttk.Combobox(win, values=[
            'Histogram of Damage Taken',
            'Bullets Fired Over Games',
            'Health Remaining by Level',
            'Grenade Usage Lineplot',
            'Deaths Per Level Analysis'
        ])
        combo.pack(pady=5)
        combo.bind("<<ComboboxSelected>>", lambda e: update_plot(combo.get()))

        fig = Figure(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack()

        # Add a Text widget to display detailed stats
        result_text = tk.Text(win, wrap=tk.WORD, height=10, width=50, font=("Arial", 10))
        result_text.pack(pady=10)

        def go_back():
            win.destroy()
            if back_callback:
                back_callback()

        tk.Button(
            win, text="BACK", command=go_back,
            font=("Arial", 16, "bold"),
            bg="gray", fg="white", activebackground="#666", activeforeground="white",
            relief=tk.FLAT, bd=0, padx=40, pady=10
        ).pack(pady=20)

        win.mainloop()


if __name__ == "__main__":
    sm = StatisticsManager()
    sm.show_all_stats()
