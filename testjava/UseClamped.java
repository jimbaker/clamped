import bar.clamped.BarClamp;  // yes, you can now just import Python classes!

public class UseClamped {

    public static void main(String[] args) {
        BarClamp barclamp = new BarClamp();
	try {
	    System.out.println("BarClamp: " + barclamp.call());
	} catch (Exception ex) {
	    System.err.println("Exception: " + ex);
	}
    }

}

