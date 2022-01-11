/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package LibTest;
import java.util.ArrayList;
//import PetriObj.PetriObjModel;
import LibNet.NetLibrary;
import PetriObj.ExceptionInvalidNetStructure;
import PetriObj.ExceptionInvalidTimeDelay;
import PetriObj.PetriObjModel;
import PetriObj.PetriSim;
import java.text.DecimalFormat;
import java.util.Collections;

/**
 *
 * @author Roman Kryvokhyzha
 */
public class lab13 {
    public static void main(String[] args) throws ExceptionInvalidTimeDelay, ExceptionInvalidNetStructure {
        period();
        double[][] factor_values = {{1.75, 1.75, 1.75},
                                    {0.25, 1.75, 1.75},
                                    {1.75, 0.25, 1.75},
                                    {0.25, 0.25, 1.75},
                                    {1.75, 1.75, 0.25},
                                    {0.25, 1.75, 0.25},
                                    {1.75, 0.25, 0.25},
                                    {0.25, 0.25, 0.25}};
        
        System.out.println();
        System.out.println("LINER REGRESSION ANALYSIS");
        linerRegressioAnalysis(factor_values);
        System.out.println();
        System.out.println("ANALYSIS OF VARIANCE");
        analysisOfVariance();      
        
    }
    
    public static void period() throws ExceptionInvalidNetStructure, ExceptionInvalidTimeDelay{
        double epsilon = 0.0005;
        
        for (int i = 0; i < 4; i++){
            ArrayList <PetriSim> list = new ArrayList <PetriSim>();
            list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(1.0, 1.0, 1.0)));
            PetriObjModel model = new PetriObjModel(list);
            model.setIsProtokol(false);
            double period = model.go(10000.0, epsilon);
            System.out.println("PERIOD: " + period);
        }        
    }
    
    public static void linerRegressioAnalysis(double[][] factor_values) throws ExceptionInvalidNetStructure, ExceptionInvalidTimeDelay{
        ArrayList<ArrayList<Double>> yValues = new ArrayList<>();        
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(factor_values[i][0],factor_values[i][1], factor_values[i][2])));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            yValues.add(y_experiment);                        
        }
        double cohranTestResult = cohranTest(yValues);
        if (cohranTestResult != 0){
            ArrayList<Double> b_values = calcBThreeFactorsTest (yValues);
            ArrayList<Boolean> studentTestResult = studentTest(b_values, cohranTestResult);
            ArrayList<String> b_mult_x = bMultX();
            ArrayList<Double> y_reg = new ArrayList<>();
            ArrayList<Double> y_j = yJValues(yValues);
            ArrayList<String> reg_equation = new ArrayList<>();
            int[][] coef_signs = coefs();
            int important = 0;
            reg_equation.add("y = ");
            
            //DecimalFormat f = new DecimalFormat("##.00");
            for (int k=0; k<studentTestResult.size(); k++){
                if (studentTestResult.get(k)==true){
                    reg_equation.add(/**f.format(b_values.get(k))*/ b_values.get(k) +b_mult_x.get(k)+ " + ");
                    important += 1;
                }
            }
            for (int k=0; k<8; k++){
                double y_reg_value = 0;
                for (int j=0; j<studentTestResult.size(); j++){
                    if (studentTestResult.get(j)==true){
                        y_reg_value += b_values.get(j) * coef_signs[k][j];                         
                    }
                }
                //System.out.println("Y_reg:"+y_reg_value);
                y_reg.add(y_reg_value);
            }
            
            for (int i = 0; i<8; i++){
                System.out.println("b" + i + "=" + b_values.get(i) + "\ty" + i + "=" + y_j.get(i) + "\ty_reg" + i + "=" + y_reg.get(i));
            }
            System.out.println();
            for (String s: reg_equation){
                System.out.print(s);
            }
            System.out.println();
            if (important < 8){
                boolean fisherTestResult = fisherTest(y_j, y_reg, cohranTestResult, important);
                if (fisherTestResult == false){
                    System.out.println("Fisher Test is not passed");
                }  
            }
            else 
                System.out.println("All factors are important - Fisher test is not needed");
        }
        else
            System.out.println("Cohran Test is not passed");
    }
    
    public static ArrayList<Double> yJValues(ArrayList<ArrayList<Double>> yValues){
        ArrayList<Double> y_j = new ArrayList<>();
        for (ArrayList<Double> y_experiment: yValues){
            double sum = 0;
            for (Double y: y_experiment){
               sum += y;
            }
            y_j.add(sum/y_experiment.size());
        }
        return y_j;         
    }
             
    public static double cohranTest(ArrayList<ArrayList<Double>> yValues){
        boolean cohranFlag = false;
        ArrayList<Double> y_j = yJValues(yValues);
        ArrayList<Double> d_j = new ArrayList<>();
        double d_sum = 0;
        for (ArrayList<Double> y_experiment: yValues){  
            double sum = 0;
            for (int i = 0; i<y_j.size(); i++){                
                for(Double y_ij: y_experiment){
                    sum += Math.pow((y_ij - y_j.get(i)), 2); 
                }
            }
            d_j.add(sum/(y_experiment.size()-1));
        }
        double d_max = Collections.max(d_j);
        for (Double d: d_j){
            d_sum += d;
        }
        if (d_max/d_sum < 0.4377){
            cohranFlag = true;
            System.out.println("G = " + d_max/d_sum + " < 0.4377 - Cohran test is passed");
        }            
        if (cohranFlag)    
            return d_sum/8;
        else 
            return 0.0;
    }   
    
    
    public static ArrayList<Double> calcBThreeFactorsTest (ArrayList<ArrayList<Double>> yValues){
        ArrayList<Double> b_values = new ArrayList<>();
        
        ArrayList<Double> y_j = new ArrayList<>();
        for (ArrayList<Double> y_experiment: yValues){
            double sum = 0;
            for (Double y: y_experiment){
                sum += y;
            }
            y_j.add(sum/y_experiment.size());
        }
        
        double y_j_sum = 0;
        for (Double y: y_j){
            y_j_sum += y;
        }
        
        int[][] coef_sign = {{1, 1, 1 , 1, 1, 1, 1, 1},
                     {1, -1, 1, 1, -1, -1, 1, -1},
                     {1, 1, -1, 1, -1, 1, -1, -1},
                     {1, -1, -1, 1, 1, -1, -1, 1},
                     {1, 1, 1, -1, 1, -1, -1, -1},
                     {1, -1, 1, -1, -1, 1, -1, 1},
                     {1, 1, -1, -1, -1, -1, 1, 1},
                     {1, -1, -1, -1, 1, 1, 1, -1}};
                
        for(int i=0; i < coef_sign.length; i++) {
            double b = 0;
            for(int j=0; j < coef_sign[i].length; j++) {
                b += y_j.get(j) * coef_sign[i][j];
            }
            b_values.add(b/8);
        }
        
        /*b_values.add(y_j_sum/8);
        b_values.add((y_j_sum - y_j.get(1) - y_j.get(3) - y_j.get(5) - y_j.get(7))/8);
        b_values.add((y_j_sum - y_j.get(2) - y_j.get(3) - y_j.get(6) - y_j.get(7))/8);
        b_values.add((y_j_sum - y_j.get(4) - y_j.get(5) - y_j.get(6) - y_j.get(7))/8);
        b_values.add((y_j_sum - y_j.get(1) - y_j.get(2) - y_j.get(5) - y_j.get(6))/8);
        b_values.add((y_j_sum - y_j.get(1) - y_j.get(3) - y_j.get(4) - y_j.get(6))/8);
        b_values.add((y_j_sum - y_j.get(2) - y_j.get(3) - y_j.get(4) - y_j.get(5))/8);
        b_values.add((y_j_sum - y_j.get(1) - y_j.get(2) - y_j.get(4) - y_j.get(7))/8);*/
                
        return b_values;
    }
    
    public static ArrayList<Boolean> studentTest(ArrayList<Double> b_values, double dispersion){
        ArrayList<Double> t_values = new ArrayList<>();
        ArrayList<Boolean> importance = new ArrayList<>();
        
        for(Double b: b_values){
            t_values.add(b * Math.sqrt(32/dispersion));
        }
        
        for (Double t: t_values){
            if (Math.abs(t) > 2.06)
                importance.add(true);
            else
                importance.add(false);
        }        
        return importance;
    } 
           
    public static boolean fisherTest(ArrayList<Double> y_j, ArrayList<Double> y_reg, double dispersion, int important){
        boolean fisherFlag = false;
        
        double d_adequacy = 0;
        for (int i=0; i<y_j.size(); i++){
            d_adequacy += Math.pow((y_j.get(i)-y_reg.get(i)), 2);
            //System.out.println(Math.pow((y_j.get(i)-y_reg.get(i)), 2));
            //System.out.println(d_adequacy);
        }
        d_adequacy /= (8-important);
        System.out.println();
        System.out.println("Dad = " + d_adequacy);
        if (d_adequacy/dispersion < 8.64){
            System.out.println(d_adequacy/dispersion + " < 8.64 - Fisher test is passed");
            fisherFlag = true;            
        }           
        else
            System.out.println(d_adequacy/dispersion + " > 8.64 - Fisher test is passed");
        return fisherFlag;
    }
    
    public static ArrayList <String> bMultX (){
        ArrayList <String> b_mult_x = new ArrayList<>() ;
        b_mult_x.add(" ");
        b_mult_x.add("x1 ");
        b_mult_x.add("x2 ");
        b_mult_x.add("x3 ");
        b_mult_x.add("x1x2 ");
        b_mult_x.add("x1x3 ");
        b_mult_x.add("x2x3 ");
        b_mult_x.add("x1x2x3 ");
        return b_mult_x;
    } 
    
    public static int[][] coefs (){
        int[][] coef_sign = {{1, 1, 1 , 1, 1, 1, 1, 1},
                             {1, -1, 1, 1, -1, -1, 1, -1},
                             {1, 1, -1, 1, -1, 1, -1, -1},
                             {1, -1, -1, 1, 1, -1, -1, 1},
                             {1, 1, 1, -1, 1, -1, -1, -1},
                             {1, -1, 1, -1, -1, 1, -1, 1},
                             {1, 1, -1, -1, -1, -1, 1, 1},
                             {1, -1, -1, -1, 1, 1, 1, -1}};
        
        return coef_sign;
    } 
    
    public static void analysisOfVariance() throws ExceptionInvalidNetStructure, ExceptionInvalidTimeDelay{
        double[] factor_1 = {0.5, 1.5};
        double[] factor_2 = {0.5, 1.5};
        
        ArrayList<Double> y_factor_1_1 = new ArrayList<>();
        ArrayList<Double> y_factor_2_1 = new ArrayList<>();
        ArrayList<Double> y_factor_12_1 = new ArrayList<>();
        ArrayList<Double> y_factor_1_2 = new ArrayList<>();
        ArrayList<Double> y_factor_2_2 = new ArrayList<>();
        ArrayList<Double> y_factor_12_2 = new ArrayList<>();
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(factor_1[0],1.0, 1.0)));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            double sum_y = 0;
            for (Double y: y_experiment){
                sum_y+=y;
            }
            y_factor_1_1.add(sum_y/4);                        
        }
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(factor_1[1],1.0, 1.0)));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            double sum_y = 0;
            for (Double y: y_experiment){
                sum_y+=y;
            }
            y_factor_1_2.add(sum_y/4);                        
        }
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(1.0, factor_1[0], 1.0)));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            double sum_y = 0;
            for (Double y: y_experiment){
                sum_y+=y;
            }
            y_factor_2_1.add(sum_y/4);                        
        }
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(1.0, factor_1[1], 1.0)));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            double sum_y = 0;
            for (Double y: y_experiment){
                sum_y+=y;
            }
            y_factor_2_2.add(sum_y/4);                        
        }
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(factor_1[0], factor_2[0], 1.0)));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            double sum_y = 0;
            for (Double y: y_experiment){
                sum_y+=y;
            }
            y_factor_12_1.add(sum_y/4);                        
        }
        
        for (int i=0; i<8; i++){
            ArrayList<Double> y_experiment = new ArrayList<>();
            for (int j=0; j<4; j++){
                ArrayList <PetriSim> list = new ArrayList <PetriSim>();
                list.add(new PetriSim(NetLibrary.CreateСonveyorSystem(factor_1[1], factor_2[1], 1.0)));
                PetriObjModel model = new PetriObjModel(list);
                model.setIsProtokol(false);
                model.go(2000.0);
                y_experiment.add(model.getListObj().get(0).getNet().getListP()[11].getMean());
                //System.out.println(model.getListObj().get(0).getNet().getListP()[11].getMean());
            }
            double sum_y = 0;
            for (Double y: y_experiment){
                sum_y+=y;
            }
            y_factor_12_2.add(sum_y/4);                        
        }
        
        double avg_f1_1 = 0;
        double avg_f1_2 = 0;
        double avg_f2_1 = 0;
        double avg_f2_2 = 0;
        double avg_f12_1 = 0;
        double avg_f12_2 = 0;
        
        for (int i = 0; i<8; i++){
            avg_f1_1 += y_factor_1_1.get(i);
            avg_f1_2 += y_factor_1_2.get(i);
            avg_f2_1 += y_factor_2_1.get(i);
            avg_f2_2 += y_factor_2_2.get(i);
            avg_f12_1 += y_factor_12_1.get(i);
            avg_f12_2 += y_factor_12_2.get(i);
        }
        avg_f1_1 /= 8;
        avg_f1_2 /= 8;
        avg_f2_1 /= 8;
        avg_f2_2 /= 8;
        avg_f12_1 /= 8;
        avg_f12_2 /= 8;
        
        double avg_f1_12 = (avg_f1_1+avg_f1_2)/2;
        double avg_f2_12 = (avg_f2_1+avg_f2_2)/2;
        double avg_f12_12 = (avg_f12_1+avg_f12_2)/2;
        
        double s_fact_1 = 8 *(Math.pow((avg_f1_1 - avg_f1_12), 2) + Math.pow((avg_f1_2 - avg_f1_12), 2));
        double s_fact_2 = 8 *(Math.pow((avg_f2_1 - avg_f2_12), 2) + Math.pow((avg_f2_2 - avg_f2_12), 2));
        double s_fact_12 = 8 *(Math.pow((avg_f12_1 - avg_f12_12), 2) + Math.pow((avg_f12_2 - avg_f12_12), 2));
        
        double s_left1 = 0;
        double s_left2 = 0;
        double s_left12 = 0;
        
        for (int i=0; i<8; i++){
            s_left1 = Math.pow((y_factor_1_1.get(i) - avg_f1_1), 2) + Math.pow((y_factor_1_2.get(i) - avg_f1_2), 2);
            s_left2 = Math.pow((y_factor_2_1.get(i) - avg_f2_1), 2) + Math.pow((y_factor_2_2.get(i) - avg_f2_2), 2);
            s_left12 = Math.pow((y_factor_12_1.get(i) - avg_f12_1), 2) + Math.pow((y_factor_12_2.get(i) - avg_f12_2), 2);
        }
        s_left1/=12;
        s_left2/=12;
        s_left12/=12;
        
        double f1 = s_fact_1/s_left1;
        double f2 = s_fact_2/s_left2;
        double f12 = s_fact_12/s_left12;
        
        System.out.println("Factor1 process time 1: ");
        System.out.println("D_fact = " + s_fact_1 + "\tD_left = " + s_left1);
        if (f1>4.747)
            System.out.print(f1 + " > 4.747 - Factor process time 1 is important");
        
        else
            System.out.print(f1 + " < 4.747 - Factor process time 1 is not important");
        System.out.println();
        System.out.println("Factor2 transition 1-2: ");
        System.out.println("D_fact = " + s_fact_2 + "\tD_left = " + s_left2);
        if (f2>4.747)
            System.out.print(f2 + " > 4.747 - Factor2 transition 1-2 is important");
        else
            System.out.print(f2 + " < 4.747 - Factor2 transition 1-2 is not important");
        System.out.println();
        System.out.println("Factor1 & Factor2: ");
        System.out.println("D_fact = " + s_fact_12 + "\tD_left = " + s_left12);
        if (f12>4.747)
            System.out.print(f12 + " > 4.747 - Factor1 & Factor2 is important");
        else
            System.out.print(f12 + " < 4.747 - Factor1 & Factor2 is not important");
        System.out.println();
    }
    
}
